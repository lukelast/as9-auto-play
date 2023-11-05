import os
import time
from typing import Optional
from functools import cached_property
from typing import List, Tuple
import cv2
import easyocr
import numpy
from mss.screenshot import ScreenShot
from numpy import ndarray

from as9.util.screen_region import ScreenRegion
from as9.util.settings import CAPTURE_DIR

# Initialize EasyOCR with English as the chosen language
reader = easyocr.Reader(['en'])

OcrResults = List[Tuple[List[List[int]], str, float]]

class Screenshot:

    def __init__(self):
        self.region: ScreenRegion = ScreenRegion()
        self.screenshot: Optional[ScreenShot] = None
        self.bgra: Optional[ndarray] = None
        self.bgr: Optional[ndarray] = None
        self.rgb: Optional[ndarray] = None
        self.gray: Optional[ndarray] = None

    def get_bgra(self):
        if self.bgra is None:
            self.bgra = numpy.array(self.screenshot)
        return self.bgra

    def get_bgr(self):
        if self.bgr is None:
            self.bgr = cv2.cvtColor(self.get_bgra(), cv2.COLOR_BGRA2BGR)
            #self.bgr = self.get_bgra()[:, :, :3]
        return self.bgr

    def get_rgb(self):
        if self.rgb is None:
            self.rgb = cv2.cvtColor(self.get_bgra(), cv2.COLOR_BGRA2RGB)
            #self.rgb = self.get_bgra()[:, :, :3][:, :, ::-1]
        return self.rgb

    def get_gray(self):
        if self.gray is None:
            self.gray = cv2.cvtColor(self.get_bgra(), cv2.COLOR_BGRA2GRAY)
        return self.gray

    def do_ocr(self) -> OcrResults:
        result: OcrResults = reader.readtext(self.get_rgb())
        result = sorted(result, key=lambda x: x[1])
        return result

    def draw_ocr(self, result: OcrResults):
        rgb = self.get_rgb()
        green = (0, 255, 0)
        line_thickness = 4
        for detection in result:
            top_left, top_right, bottom_right, bottom_left = detection[0]
            x1, y1 = tuple(map(int, top_left))
            x2, y2 = tuple(map(int, bottom_right))
            cv2.rectangle(rgb, (x1, y1), (x2, y2), green, line_thickness)
        self.bgra = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGRA)
        self.bgr = None
        self.gray = None

    def save(self,
             directory: str,
             name: str,
             timestamp: bool = True,
             quality: int = 100
             ):
        _dir = f"{CAPTURE_DIR}/{directory}"
        if not os.path.exists(_dir):
            os.makedirs(_dir)
        if timestamp:
            name = f"{name}-{int(time.time())}"

        if quality == 100:
            cv2.imwrite(f"{_dir}/{name}.png", self.get_bgr())
        else:
            cv2.imwrite(f"{_dir}/{name}.jpg", self.get_bgr(), [cv2.IMWRITE_JPEG_QUALITY, quality])
