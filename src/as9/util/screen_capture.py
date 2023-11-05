import os
import time

import cv2
import mss
import pyscreeze
import numpy

from as9.util.screen_region import ScreenRegion
from as9.util.screenshot import Screenshot
from as9.util.settings import CAPTURE_DIR


class ScreenCapture:

    def __init__(self, color: bool = False):
        self.color = color
        self.region: ScreenRegion = ScreenRegion()

    def screenshot(self) -> Screenshot:
        shot = self._screenshot_mss()
        shot.region = self.region
        return shot

    def _screenshot_pyscreeze(self):
        region = self.region
        region_tuple = (region['left'], region['top'], region['width'], region['height'])
        screenshot = pyscreeze.screenshot(region=region_tuple)
        screen_np = numpy.array(screenshot)
        gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
        return gray

    def _screenshot_mss(self) -> Screenshot:
        screenshot = Screenshot()
        with mss.mss() as sct:
            screenshot.screenshot = sct.grab(self.region.region)
        return screenshot

    def _screenshot_imread(self):
        region = self.region
        left = region['left']
        top = region['top']
        width = region['width']
        height = region['height']
        screen_np = cv2.imread(f"{CAPTURE_DIR}/race-4k.png")
        gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
        gray_cropped = gray[top:top + height, left:left + width]
        return gray_cropped


def save_jpg(image, directory: str, name: str, timestamp: bool = True):
    _dir = f"{CAPTURE_DIR}/{directory}"
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    if timestamp:
        name = f"{int(time.time())}-{name}"
    file_name = f"{_dir}/{name}.jpg"
    cv2.imwrite(file_name, image, [cv2.IMWRITE_JPEG_QUALITY, 20])


def save_png(image, dir: str, name: str):
    _dir = f"{CAPTURE_DIR}/{dir}"
    if not os.path.exists(_dir):
        os.makedirs(_dir)
    cv2.imwrite(f"{_dir}/{int(time.time())}-{name}.png", image)
