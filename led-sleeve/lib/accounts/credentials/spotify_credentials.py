from .credentials import Credentials

class SpotifyCredentials(Credentials):
    @property
    def access_token(self):
        return self._account['credentials']['access_token']

    @property
    def refresh_token(self):
        return self._account['credentials']['refresh_token']

    def update(self, access_token, refresh_token=None):
        if refresh_token is None:
            refresh_token = self.refresh_token

        self._account['credentials'] = {
            'access_token': access_token, 'refresh_token': refresh_token}
        self.store_credentials()
