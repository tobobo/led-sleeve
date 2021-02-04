from .tokens import Tokens
from .keys import Keys
from .accounts.spotify_account import SpotifyAccount


class AccountConfig():
    def __init__(self):
        self._accounts = None

    async def load(self):
        keys = Keys()
        keys.load()
        tokens = Tokens()
        tokens.load()
        self._accounts = [SpotifyAccount(keys, tokens)]

    async def get_accounts(self):
        return self._accounts
