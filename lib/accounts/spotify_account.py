
import sys
import logging
import asyncio
import requests
import aiohttp
import aiohttp_client
from .account import Account


class SpotifyAccount(Account):
    def __init__(self, keys, tokens=None):
        self._keys = keys
        self._tokens = tokens
        self._current_image_url = None
        self._poll_time = 5
        self._timeout = aiohttp.ClientTimeout(total=10)
        self.now_playing_state = []
        super().__init__()

    def get_image_url(self, response_data):
        if not response_data:
            return None
        elif len(response_data['album']['images']) > 0:
            print(response_data)
            return response_data['album']['images'][0]['url']
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

    def get_auth_headers(self):
        return {
            'Authorization': f'Bearer {self._tokens.access_token}'
        }

    async def reauthorizing_request(self, method, *args, **kwargs):
        while True:
            try:
                response = await method(*args, **kwargs)
                if response.status == 401:
                    await self.reauthorize()
                else:
                    return response
            except requests.exceptions.RequestException:
                logging.exception('error making spotify request')
                await asyncio.sleep(self._poll_time)

    async def get_now_playing(self):
        response = await self.reauthorizing_request(
            aiohttp_client.get,
            'https://api.spotify.com/v1/me/player/currently-playing',
            params={ 'market': 'from_token' },
            headers=self.get_auth_headers(),
            timeout=self._timeout
        )
        if response.status == 200:
            now_playing_data = await response.json()
            logging.debug(response.url)
            logging.debug(now_playing_data)
            if not now_playing_data['is_playing']:
                return None
            track_id = now_playing_data['item']['id']
            track_response = await self.reauthorizing_request(
                aiohttp_client.get,
                f'https://api.spotify.com/v1/tracks/{track_id}',
                params={ 'market': 'from_token' },
                headers=self.get_auth_headers(),
                timeout=self._timeout
            )
            track_data = await track_response.json()
            logging.debug(track_response.url)
            logging.debug(track_data)
            return track_data
        elif response.status == 204:
            logging.info('no spotify track')
            return None
        else:
            logging.info('some unknown response when getting track')
            logging.debug(response.status)
            logging.debug(response.text)
            return None

    async def wait_for_updates(self):
        while True:
            try:
                response_data = await self.get_now_playing()
                image_url = self.get_image_url(response_data)
                logging.info("image url: %s", image_url)

                if image_url is not None and image_url != self._current_image_url:
                    self._current_image_url = image_url
                    self.now_playing_state = [image_url]
                    await self.send_update(image_url)
                elif image_url is None:
                    logging.debug("sending black screen to display proc")
                    self._current_image_url = None
                    self.now_playing_state = [None]
                    await self.send_update(None)

            except KeyboardInterrupt:
                sys.exit(0)
            except Exception:
                logging.exception('error updating spotify state')
            await asyncio.sleep(5)
