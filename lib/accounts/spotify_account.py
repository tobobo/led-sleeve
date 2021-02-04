
import sys
import traceback
import logging
import asyncio
import requests
from requests.auth import HTTPBasicAuth
from .account import Account


class SpotifyAccount(Account):
    def __init__(self, keys, tokens=None):
        self._keys = keys
        self._tokens = tokens
        self._current_image_url = None
        self._poll_time = 5
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
        try:
            auth_response = requests.post(
                'https://accounts.spotify.com/api/token',
                data={
                    'grant_type': 'refresh_token', 'refresh_token': self._tokens.refresh_token
                },
                auth=HTTPBasicAuth(self._keys.client_id,
                                   self._keys.client_secret)
            )
            auth_response_data = auth_response.json()
            print(auth_response_data)
            access_token = auth_response_data['access_token']
            refresh_token = self._tokens.refresh_token
            if 'refresh_token' in auth_response_data:
                print('got refresh token')
                refresh_token = auth_response_data['refresh_token']
            self._tokens.update(access_token, refresh_token)
        except KeyboardInterrupt:
            sys.exit(0)
        except Exception as err:
            print('error reauthorizing')
            traceback.print_exc()
            raise err
    
    def get_auth_headers(self):
        return {
            'Authorization': f'Bearer {self._tokens.access_token}'
        }

    async def reauthorizing_request(self, method, *args, **kwargs):
        while True:
            try:
                response = method(*args, **kwargs)
                if response.status_code == 401:
                    await self.reauthorize()
                else:
                    return response
            except requests.exceptions.RequestException:
                traceback.print_exc()
                await asyncio.sleep(self._poll_time)

    async def get_now_playing(self):
        response = await self.reauthorizing_request(requests.get, 'https://api.spotify.com/v1/me/player/currently-playing?market=from_token', headers=self.get_auth_headers(), timeout=10)
        if response.status_code == 200:
            now_playing_data = response.json()
            if not now_playing_data['is_playing']:
                return None
            track_id = now_playing_data['item']['id']
            print(f'track id: {track_id}')
            track_response = await self.reauthorizing_request(requests.get, f'https://api.spotify.com/v1/tracks/{track_id}?market=from_token', headers=self.get_auth_headers(), timeout=10)
            return track_response.json()
        elif response.status_code == 204:
            print('no track')
            return None
        else:
            print('some unknown response when getting track')
            print(response.status_code)
            print(response.text)
            return None

    async def wait_for_updates(self):
        while True:
            try:
                response_data = await self.get_now_playing()
                image_url = self.get_image_url(response_data)
                logging.debug(f"image url: {image_url}")

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
            except:
                print('error updating')
                traceback.print_exc()
            await asyncio.sleep(5)
