#!/usr/bin/env python3

import asyncio
import logging
from lib.display.display_interface import DisplayInterface
from lib.display.image_preparer import ImagePreparer
from lib.display.display_mediator import DisplayMediator
from lib.accounts.now_playing import NowPlaying
from lib.web.server import start_server

logging.basicConfig(level=logging.DEBUG)

display = DisplayInterface()
image_preparer = ImagePreparer()
now_playing = NowPlaying()

display_mediator = DisplayMediator(now_playing, image_preparer, display)

async def main():
    await asyncio.gather(
        now_playing.wait_for_updates(),
        start_server()
    )

if __name__ == "__main__":
    asyncio.run(main())
