from .tokens import Tokens
from .keys import Keys
from .spotify_account import SpotifyAccount


class AccountConfig():
    def __init__(self):
        self._accounts = None

    async def load(self):
        keys = Keys()
        keys.load()
        tokens = Tokens()
        tokens.load()
        self._accounts = [SpotifyAccount(keys, tokens)]
    
    async def ensure_loaded(self):
        if self._accounts is None:
            await self.load()

    async def get_accounts(self):
        await self.ensure_loaded()
        return self._accounts
