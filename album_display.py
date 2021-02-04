import sys
import time
import logging
import os
import time
import gc
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent, FileDeletedEvent, FileModifiedEvent
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from gamma_correction import process
from PIL import Image, ImageEnhance

options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.limit_refresh_rate_hz = 80
options.scan_mode = 1

matrix = RGBMatrix(options=options)
# matrix.brightness = 85

black = Image.new('RGB', (64, 64))

logging.debug("album display python2 proc started")

def correct_gamma_and_resize(img):
    img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    return process(img)

ENHANCERS = [
  (ImageEnhance.Color, 1.1),
  (ImageEnhance.Brightness, 0.8),
  (ImageEnhance.Contrast, 1.1)
]

def correct_with_pil(img):
    for Enhancer, amt in ENHANCERS:
      enhancer = Enhancer(img)
      img = enhancer.enhance(amt)
    img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    return img


def display_image(path):
    image = Image.open(path)
    corrected = correct_with_pil(image)
    matrix.SetImage(corrected.convert('RGB'))


def display_black():
    matrix.SetImage(black)

if __name__ == "__main__":
    while True:
      for line in iter(sys.stdin.readline, ''):
        path = line[:-1]
        if path:
          logging.debug("displaying {}".format(path))
          display_image(path)
        else:
          logging.debug("showing black screen")
          display_black()
      time.sleep(5)
