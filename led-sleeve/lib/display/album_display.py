import sys
import time
import logging
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
# options.limit_refresh_rate_hz = 80
# options.scan_mode = 1

matrix = RGBMatrix(options=options)
matrix.brightness = 85

black = Image.new('RGB', (64, 64))

logging.debug("album display python2 proc started")


def display_image(image_path):
    image = Image.open(image_path)
    matrix.SetImage(image.convert('RGB'))


def display_black():
    matrix.SetImage(black)


if __name__ == "__main__":
    while True:
        for line in iter(sys.stdin.readline, ''):
            image_path = line[:-1]
            if image_path:
                logging.debug("displaying {}".format(image_path))
                display_image(image_path)
            else:
                logging.debug("showing black screen")
                display_black()
        time.sleep(5)
