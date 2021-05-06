# wtf...
import sys
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from config import config
from lib.display.display_interface import DisplayInterface
from pi_wifi_bootstrap.pi_wifi_bootstrap import run_wifi_bootstrap
import qrcode
import logging
import asyncio
import os



this_dir = os.path.dirname(os.path.realpath(__file__))

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s', level=logging.DEBUG)

display = DisplayInterface()


def on_start_app():
    logging.debug("on start app")
    asyncio.create_task(display.stop())
    
def center_text(text):
    return (63 - (len(text) * 4 - 1)) / 2

def on_create_ap():
    qr = qrcode.QRCode(
        box_size=1,
        border=2,
    )
    qr.add_data(
        f'{config.auth_site_base}/{config.device_name}?psk={config.ap_psk}')
    img = qr.make_image()
    img_path = f'{this_dir}/data/ap_qr.jpg'
    img.save(img_path, 'JPEG')
    logging.debug(img.width)
    logging.debug(img.border)
    text = 'set up wifi'
    asyncio.create_task(display.send([
        {
            'type': 'image',
            'path': img_path,
            'position': ((63 - (img.width + (img.border * 2))) / 2, 5),
            'brightness': 65535
        },
        {
            'type': 'text',
            'text': text,
            'position': (0, 54),
            'position': (center_text(text), 54)
        }
    ]))


def on_check_wifi_connection():
    logging.debug("on check wifi")
    texts = ['looking', 'for', 'wifi...']
    asyncio.create_task(display.send([
        {
            'type': 'brightness',
            'brightness': 'min'
        },
        {
            'type': 'text',
            'text': texts[0],
            'position': (center_text(texts[0]) + 1, 24)
        },
        {
            'type': 'text',
            'text': texts[1],
            'position': (center_text(texts[1]) + 1, 30)
        },
        {
            'type': 'text',
            'text': texts[2],
            'position': (center_text(texts[2]) + 1, 36)
        },
    ]))


async def start():
    await display.ensure_display_proc()
    await run_wifi_bootstrap(
        ".",
        "sudo python3 -u led_sleeve.py",
        on_create_ap=on_create_ap,
        on_check_wifi_connection=on_check_wifi_connection,
        on_start_app=on_start_app
    )

if __name__ == "__main__":
    asyncio.run(start())
