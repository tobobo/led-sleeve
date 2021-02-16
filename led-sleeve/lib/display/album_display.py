import sys
import time
import logging
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

logging.basicConfig(level=logging.INFO)

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 2
# options.limit_refresh_rate_hz = 70
# options.scan_mode = 1

matrix = RGBMatrix(options=options)
MAX_BRIGHTNESS = 100
MIN_BRIGHTNESS = 80
BRIGHTNESS_CURVE_POWER = 2
matrix.brightness = MAX_BRIGHTNESS

black = Image.new('RGB', (64, 64))

logging.debug("album display python2 proc started")


def display_image(image_path):
    image = Image.open(image_path)
    matrix.SetImage(image.convert('RGB'))


def display_black():
    matrix.SetImage(black)


MAX_IMAGE_BRIGHTNESS = 65535


def caculate_matrix_brightness(brightness):
    # all white image would be at the dimmest level
    # all black at the brightest
    logging.debug("input brightness %s", brightness)
    display_brightness = MAX_BRIGHTNESS - \
        (brightness / MAX_IMAGE_BRIGHTNESS) ** BRIGHTNESS_CURVE_POWER * \
        (MAX_BRIGHTNESS - MIN_BRIGHTNESS)
    logging.debug("output brightness %s", display_brightness)
    return display_brightness


if __name__ == "__main__":
    while True:
        for line in iter(sys.stdin.readline, ''):
            message = line[:-1]
            if message:
                [image_path, brightness_str] = message.split()
                image_brightness = float(brightness_str)
                matrix.brightness = caculate_matrix_brightness(image_brightness)
                logging.debug("displaying {}".format(image_path))
                display_image(image_path)
            else:
                logging.debug("showing black screen")
                display_black()
        time.sleep(5)
