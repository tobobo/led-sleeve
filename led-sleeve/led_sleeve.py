
# wtf...
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')

from initialize import initialize
from lib.display.display_interface import DisplayInterface
from lib.display.image_preparer import ImagePreparer
from lib.display.display_mediator import DisplayMediator
from lib.database import Database
from lib.accounts.now_playing import NowPlaying
from lib.web.server import start_server

print("starting")

if __name__ == "__main__":
    initialize(
        DisplayInterface=DisplayInterface,
        ImagePreparer=ImagePreparer,
        DisplayMediator=DisplayMediator,
        Database=Database,
        NowPlaying=NowPlaying,
        start_server=start_server
    )
