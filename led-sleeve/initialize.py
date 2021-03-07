import asyncio
import logging
import os

from dotenv import load_dotenv


load_dotenv()

logging.basicConfig(level=logging.DEBUG)

print(os.getenv('AUTH_SITE_BASE'))

async def start(now_playing, start_server, database):
    await asyncio.gather(
        now_playing.wait_for_updates(),
        start_server(database, now_playing)
    )

def initialize( # pylint: disable=too-many-arguments,invalid-name
  DisplayInterface,
  ImagePreparer,
  DisplayMediator,
  Database,
  NowPlaying,
  start_server
):
    database = Database()
    display = DisplayInterface()
    image_preparer = ImagePreparer()
    now_playing = NowPlaying(database)

    DisplayMediator(now_playing, image_preparer, display)

    asyncio.run(start(now_playing, start_server, database))
