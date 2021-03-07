
import sys
import os
import logging
import asyncio
import aiohttp
import aiohttp_client
from .account import Account
from .keys import Keys

keys = Keys()
keys.load()

TIMEOUT = aiohttp.ClientTimeout(total=10)


class SpotifyAccount(Account):
    def __init__(self, account_id, credentials=None):
        self.provider = 'spotify'
        self.id = account_id
        self._credentials = credentials
        self._current_image_url = None
        self._poll_time = 5
        self.now_playing_state = None
        self._task = None
        super().__init__()

    @staticmethod
    async def create(creation_data):
        token_response = await aiohttp_client.post(
            'https://accounts.spotify.com/api/token',
            data={
                'grant_type': 'authorization_code',
                'code': creation_data['code'],
                'redirect_uri': f'{os.getenv("AUTH_SITE_BASE")}/authcb/spotify',
            },
            auth=aiohttp.BasicAuth(keys.client_id,
                                   keys.client_secret),
            timeout=TIMEOUT
        )
        response_data = await token_response.json()
        logging.debug(response_data)
        access_token = response_data['access_token']
        refresh_token = response_data['refresh_token']
        account_response = await aiohttp_client.get(
            'https://api.spotify.com/v1/me',
            headers={
                'Authorization': f'Bearer {access_token}'
            }
        )
        account_response_data = await account_response.json()
        return {
            'provider': 'spotify',
            'id': account_response_data['id'],
            'credentials': {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        }

    def get_image_url(self, track_data):
        if not track_data:
            return None
        elif len(track_data['album']['images']) > 0:
            return track_data['album']['images'][0]['url']
        else:
            return None

    async def reauthorize(self):
        logging.info('reauthorizing spotify')
        try:
            response = await aiohttp_client.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'refresh_token', 'refresh_token': self._credentials.refresh_token
                },
                auth=aiohttp.BasicAuth(keys.client_id,
                                       keys.client_secret),
                timeout=TIMEOUT
            )
            response_text = await response.text()
            logging.debug(response_text)
            response_data = await response.json()
            logging.debug(response.url)
            logging.debug(response_data)
            access_token = response_data['access_token']
            refresh_token = self._credentials.refresh_token
            if 'refresh_token' in response_data:
                logging.info('got new refresh token')
                refresh_token = response_data['refresh_token']
            self._credentials.update(access_token, refresh_token)
        except Exception as err:
            logging.exception('error reauthorizing')
            raise err

    async def authorized_request(self, method, *args, **kwargs):
        while True:
            kwargs['headers'] = kwargs['headers'] if 'headers' in kwargs else {}
            kwargs['headers']['Authorization'] = \
                kwargs['headers']['Authorization'] if 'authorization' in kwargs['headers'] \
                else f'Bearer {self._credentials.access_token}'
            kwargs['timeout'] = kwargs['timeout'] if 'timeout' in kwargs else TIMEOUT
            try:
                response = await method(*args, **kwargs)
                if response.status == 401:
                    await self.reauthorize()
                else:
                    return response
            except aiohttp.ClientError:
                logging.exception('error making spotify request')
                await asyncio.sleep(self._poll_time)

    async def request_currently_playing(self):
        response = await self.authorized_request(
            aiohttp_client.get,
            'https://api.spotify.com/v1/me/player/currently-playing',
            params={'market': 'from_token'},
        )
        if response.status == 200:
            response_data = await response.json()
            logging.debug(response.url)
            logging.debug(response_data)
            if response_data['is_playing']:
                return response_data['item']
            else:
                return None
        elif response.status == 204:
            logging.info('no spotify track')
            return None
        else:
            logging.info('some unknown response when getting track')
            logging.debug(response.status)
            logging.debug(response.text)
            return None

    async def request_track(self, track_id):
        response = await self.authorized_request(
            aiohttp_client.get,
            f'https://api.spotify.com/v1/tracks/{track_id}',
            params={'market': 'from_token'}
        )
        track_data = await response.json()
        logging.debug(response.url)
        logging.debug(track_data)
        return track_data

    async def fetch_now_playing(self):
        playing_item = await self.request_currently_playing()
        if playing_item is None:
            return None
        track_id = playing_item['id']
        return await self.request_track(track_id)

    async def get_now_playing(self):
        if self._task is not None and not self._task.done():
            await self._task
        return self.now_playing_state

    async def update_once(self):
        response_data = await self.fetch_now_playing()
        image_url = self.get_image_url(response_data)
        logging.debug("image url: %s", image_url)

        if image_url != self._current_image_url:
            if image_url is None:
                logging.info("spotify paused")
                self._current_image_url = None
                self.now_playing_state = None
                await self.send_update(None)
            else:
                logging.info("spotify playing %s", image_url)
                self._current_image_url = image_url
                self.now_playing_state = {
                    'image_url': image_url
                }
                await self.send_update(self.now_playing_state)

    async def wait_for_updates(self):
        while True:
            try:
                self._task = asyncio.create_task(self.update_once())
                await self._task
                self._task = None

            except KeyboardInterrupt:
                sys.exit(0)
            except Exception:
                logging.exception('error updating spotify state')
            await asyncio.sleep(5)
