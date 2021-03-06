from .tokens import Tokens
from .keys import Keys
from .spotify_account import SpotifyAccount


class AccountConfig():
    def __init__(self, database):
        self._database = database
        self._accounts = None

    def create_account_interface(self, account):
        if account['provider'] == 'spotify':
            keys = Keys()
            keys.load()
            tokens = Tokens(self._database, account)
            return SpotifyAccount(tokens)

        provider = account['provider']
        raise ValueError(f'unknown provider "{provider}"')

    async def load(self):
        accounts_data = self._database.get_accounts()
        self._accounts = list(map(self.create_account_interface, accounts_data))

    async def ensure_loaded(self):
        if self._accounts is None:
            await self.load()

    async def get_accounts(self):
        await self.ensure_loaded()
        return self._accounts
