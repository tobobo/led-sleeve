
import sys
import logging
import asyncio
import aiohttp
import aiohttp_client
from .account import Account


class SpotifyAccount(Account):
    def __init__(self, keys, tokens=None):
        self.service_name = 'Spotify'
        self._keys = keys
        self._tokens = tokens
        self._current_image_url = None
        self._poll_time = 5
        self._timeout = aiohttp.ClientTimeout(total=10)
        self.now_playing_state = []
        super().__init__()

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
                    'grant_type': 'refresh_token', 'refresh_token': self._tokens.refresh_token
                },
                auth=aiohttp.BasicAuth(self._keys.client_id,
                                       self._keys.client_secret),
                timeout=self._timeout
            )
            response_text = await response.text()
            logging.debug(response_text)
            response_data = await response.json()
            logging.debug(response.url)
            logging.debug(response_data)
            access_token = response_data['access_token']
            refresh_token = self._tokens.refresh_token
            if 'refresh_token' in response_data:
                logging.info('got new refresh token')
                refresh_token = response_data['refresh_token']
            self._tokens.update(access_token, refresh_token)
        except Exception as err:
            logging.exception('error reauthorizing')
            raise err

    async def authorized_request(self, method, *args, **kwargs):
        while True:
            kwargs['headers'] = kwargs['headers'] if 'headers' in kwargs else {}
            kwargs['headers']['Authorization'] = \
                kwargs['headers']['Authorization'] if 'authorization' in kwargs['headers'] \
                else f'Bearer {self._tokens.access_token}'
            kwargs['timeout'] = kwargs['timeout'] if 'timeout' in kwargs else self._timeout
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

    async def get_now_playing(self):
        playing_item = await self.request_currently_playing()
        if playing_item is None:
            return None
        track_id = playing_item['id']
        return await self.request_track(track_id)

    async def wait_for_updates(self):
        while True:
            try:
                response_data = await self.get_now_playing()
                image_url = self.get_image_url(response_data)
                logging.debug("image url: %s", image_url)

                if image_url != self._current_image_url:
                    if image_url is None:
                        logging.info("spotify paused")
                        self._current_image_url = None
                        self.now_playing_state = [None]
                        await self.send_update(None)
                    else:
                        logging.info("spotify playing %s", image_url)
                        self._current_image_url = image_url
                        self.now_playing_state = [image_url]
                        await self.send_update(image_url)

            except KeyboardInterrupt:
                sys.exit(0)
            except Exception:
                logging.exception('error updating spotify state')
            await asyncio.sleep(5)
