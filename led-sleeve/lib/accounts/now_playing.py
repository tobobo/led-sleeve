import asyncio
import logging
from .account_config import AccountConfig


def never():
    try:
        return never.never
    except AttributeError:
        never.never = asyncio.Future()
        return never.never


class NowPlaying():
    def __init__(self, database):
        self._database = database
        self._update_handler = None
        self._accounts = None
        self.now_playing_state = None
        self._now_playing_account = None
        self._account_config = AccountConfig(database)
        self._task = None

    async def load_accounts(self):
        self._accounts = await self._account_config.get_accounts()

    async def get_accounts(self):
        if self._accounts is None:
            await self.load_accounts()
        return self._accounts

    async def get_account(self, provider, account_id):
        accounts = await self.get_accounts()
        account = next(
            (account for account in accounts if account.provider ==
             provider and account.id == account_id),
            None
        )
        if account is None:
            return None
        return account

    async def get_account_and_wait_for_status(self, provider, account_id):
        account = await self.get_account(provider, account_id)
        if account is None:
            return None
        await account.get_now_playing()
        return account

    def on_update(self, handler):
        async def async_handler(*args):
            if asyncio.iscoroutinefunction(handler):
                return await handler(*args)
            else:
                return handler(*args)
        self._update_handler = async_handler

    async def send_update(self, *args):
        await self._update_handler(*args)

    async def handle_playing_account(self, account_index, now_playing_state):
        logging.debug("got state %s, %s", now_playing_state, self._now_playing_account)
        if self._now_playing_account is None or self._now_playing_account >= account_index:
            logging.debug("updating state for this account")
            self.now_playing_state = now_playing_state
            self._now_playing_account = account_index
            await self.send_update(now_playing_state)

    async def handle_paused_account(self, account_index):
        if self._now_playing_account == account_index:
            logging.debug("now_playing: pausing account")
            for i, account in enumerate(self._accounts[account_index + 1:]):
                if account.now_playing_state:
                    self.now_playing_state = account.now_playing_state
                    self._now_playing_account = i
                    self.send_update(*account.now_playing_state)
                    return
            self.now_playing_state = None
            self._now_playing_account = None
            await self.send_update(None)

    def create_account_update_handler(self, account_index):
        async def handle_account_update(now_playing_state):
            if now_playing_state is not None:
                await self.handle_playing_account(account_index, now_playing_state)
            else:
                await self.handle_paused_account(account_index)
        return handle_account_update

    async def reload_accounts(self):
        if self._task is not None:
            self._task.cancel()
        await self._account_config.load()
        await self.load_accounts()

    async def wait_for_updates(self):
        accounts = await self.get_accounts()
        coroutines = []
        for i, account in enumerate(accounts):
            account_update_handler = self.create_account_update_handler(i)
            account.on_update(account_update_handler)
            coroutines.append(account.wait_for_updates())

        if len(coroutines) == 0:
            self._task = await never()
        else:
            self._task = await asyncio.gather(*coroutines)
