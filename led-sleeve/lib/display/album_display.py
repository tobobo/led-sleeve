import sys
import time
import logging
import json
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image

logging.basicConfig(level=logging.DEBUG)

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 5
# options.limit_refresh_rate_hz = 70
# options.scan_mode = 1

matrix = RGBMatrix(options=options)
MAX_BRIGHTNESS = 100
MIN_BRIGHTNESS = 55
BRIGHTNESS_CURVE_POWER = 2
matrix.brightness = MAX_BRIGHTNESS

logging.debug("album display python2 proc started")

font = graphics.Font()
font.LoadFont('./lib/rpi-rgb-led-matrix/fonts/4x6.bdf')

white = graphics.Color(255, 255, 255)


def display_idle():
    matrix.Clear()
    matrix.brightness = 3
    white = graphics.Color(255, 255, 255)
    graphics.DrawLine(matrix, 0, 0, 0, 63, white)
    graphics.DrawLine(matrix, 0, 63, 63, 63, white)
    graphics.DrawLine(matrix, 63, 63, 63, 0, white)
    graphics.DrawLine(matrix, 63, 0, 0, 0, white)


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
    
def handle_image(img_message):
    image_path = img_message['path']
    position = img_message['position']
    image_brightness = img_message['brightness'] if 'brightness' in img_message else MAX_BRIGHTNESS
    matrix.brightness = caculate_matrix_brightness(image_brightness)
    logging.debug("displaying {}".format(image_path))
    image = Image.open(image_path)
    matrix.SetImage(image.convert('RGB'), position[0], position[1])
    
def handle_text(text_message):
    text = text_message['text']
    position = text_message['position']
    graphics.DrawText(matrix, font, position[0], position[1], white, text)

def handle_brightness(brightness_message):
    brightness = brightness_message['brightness']
    if brightness == 'min':
        brightness = MIN_BRIGHTNESS
    elif brightness == 'max':
        brightness = MAX_BRIGHTNESS
    matrix.brightness = brightness

def handle_clear(_):
    display_idle()

message_handlers = {
    'image': handle_image,
    'text': handle_text,
    'brightness': handle_brightness,
    'clear': handle_clear,
}

if __name__ == "__main__":
    display_idle()
    while True:
        for line in iter(sys.stdin.readline, ''):
            message_str = line[:-1]
            logging.debug('MESSAGE STR')
            logging.debug(message_str)
            if message_str:
                message = json.loads(message_str)
                matrix.Clear()
                for part in message:
                    part_type = part['type']
                    handler = message_handlers[part_type]
                    handler(part)
        time.sleep(5)
