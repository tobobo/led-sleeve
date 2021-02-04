#!/usr/bin/env python3

import asyncio
import logging
from lib.display import Display
from lib.image_preparer import ImagePreparer
from lib.now_playing import NowPlaying
from lib.display_mediator import DisplayMediator

logging.basicConfig(level=logging.DEBUG)

display = Display()
image_preparer = ImagePreparer()
now_playing = NowPlaying()

display_mediator = DisplayMediator(image_preparer, display)

now_playing.on_update(display_mediator.handle_image_update)

async def main():
    await asyncio.gather(
        now_playing.wait_for_updates()
    )

if __name__ == "__main__":
    asyncio.run(main())
