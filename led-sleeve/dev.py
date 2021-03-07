#!/usr/bin/env python3

import logging
from initialize import initialize
from lib.display.display_mediator import DisplayMediator
from lib.accounts.now_playing import NowPlaying
from lib.database import Database
from lib.web.server import start_server


class FakeDisplayInterface:
    async def display_image_file(self, path, brightness):
        logging.debug("fake display: %s, %s", path, brightness)

    async def display_nothing(self):
        logging.debug("fake display off")


class FakeImagePreparer:
    async def prepare(self, image_url):
        return image_url, 100

if __name__ == "__main__":
    initialize(
        DisplayInterface=FakeDisplayInterface,
        ImagePreparer=FakeImagePreparer,
        DisplayMediator=DisplayMediator,
        Database=Database,
        NowPlaying=NowPlaying,
        start_server=start_server
    )
