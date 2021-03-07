class Credentials():
    def __init__(self, database, account):
        self._database = database
        self._account = account

    @property
    def access_token(self):
        return self._account['credentials']['access_token']

    @property
    def refresh_token(self):
        return self._account['credentials']['refresh_token']

    def store_credentials(self):
        self._database.update_account_credentials(
            self._account['provider'], self._account['id'], self._account['credentials'])

    def update(self, access_token, refresh_token=None):
        if refresh_token is None:
            refresh_token = self.refresh_token

        self._account['credentials'] = {
            'access_token': access_token, 'refresh_token': refresh_token}
        self.store_credentials()
