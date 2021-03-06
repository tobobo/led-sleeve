#!/usr/bin/env python3

import asyncio
import logging
from lib.display.display_mediator import DisplayMediator
from lib.accounts.now_playing import NowPlaying
from lib.database import Database
from lib.web.server import start_server

logging.basicConfig(level=logging.DEBUG)


class FakeDisplayInterface:
    async def display_image_file(self, path, brightness):
        logging.debug("fake display: %s, %s", path, brightness)

    async def display_nothing(self):
        logging.debug("fake display off")


class FakeImagePreparer:
    async def prepare(self, image_url):
        return image_url, 100

database = Database()
display = FakeDisplayInterface()
image_preparer = FakeImagePreparer()
now_playing = NowPlaying(database)

display_mediator = DisplayMediator(now_playing, image_preparer, display)


async def main():
    await asyncio.gather(
        now_playing.wait_for_updates(),
        start_server(database, now_playing)
    )

if __name__ == "__main__":
    asyncio.run(main())
