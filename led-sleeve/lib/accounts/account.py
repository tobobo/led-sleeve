import asyncio


class Account():
    def __init__(self):
        self._update_handler = None
        self.now_playing_state = None

    def on_update(self, handler):
        async def async_handler(*args):
            if asyncio.iscoroutinefunction(handler):
                return await handler(*args)
            else:
                return handler(*args)
        self._update_handler = async_handler

    async def send_update(self, now_playing_state):
        self.now_playing_state = now_playing_state
        await self._update_handler(now_playing_state)

    async def wait_for_updates(self):
        pass
