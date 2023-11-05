import logging
import time

import PIL.Image
import cv2
import numpy as np
import pyautogui
import pyscreeze

from as9.util.settings import CAPTURE_DIR
from as9.util.settings import IMG_DIR
from as9.util.settings import debug_save_screen_images
from as9.util.utils import ImageNotFound

screen_width = pyscreeze.screenshot().width
# This is the resolution that the images were captured at.
STANDARD_SCREEN_WIDTH = 3840


class NeedleImg:
    USE_GRAYSCALE = True
    MIN_CONFIDENCE = 0.5

    def __init__(self, needle_img: str, threshold: float = 0.8):
        self.needle_img_name: str = needle_img
        self.needle_img_rgb = None
        self.needle_img_gray = None
        self.needle_h = None
        self.needle_w = None

        self.screenshot: PIL.Image.Image
        self.screenshot_rgb = None
        self.screenshot_gray = None

        assert self.MIN_CONFIDENCE <= threshold <= 1.0
        self.threshold: float = threshold
        self.result_boxes: list[ResultBox] = []

        self.load_needle()

    def save_screen_to_file(self, msg: str = "screenshot"):
        self.render_results()
        image_path = f"{CAPTURE_DIR}/" \
                     f"{int(time.time())}-{self.needle_img_name.replace('/', '-')}-{msg}-{self.best_confidence_int()}.jpg"
        half_size_rgb = cv2.resize(self.screenshot_rgb, None, fx=0.5, fy=0.5,
                                   interpolation=cv2.INTER_AREA)
        cv2.imwrite(image_path, half_size_rgb)

    def capture_screen(self):
        self.screenshot = None
        self.screenshot_rgb = None
        self.screenshot_gray = None
        self.result_boxes = []
        self.screenshot = pyscreeze.screenshot()
        screenshot_np = np.array(self.screenshot)
        self.screenshot_rgb = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
        self.screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

    def load_needle(self):
        self.needle_img_rgb = cv2.imread(f"{IMG_DIR}/{self.needle_img_name}.png", cv2.IMREAD_COLOR)
        if screen_width != STANDARD_SCREEN_WIDTH:
            scale = screen_width / STANDARD_SCREEN_WIDTH
            self.needle_img_rgb = cv2.resize(self.needle_img_rgb, None, fx=scale, fy=scale,
                                             interpolation=cv2.INTER_AREA)
        self.needle_img_gray = cv2.cvtColor(self.needle_img_rgb, cv2.COLOR_BGR2GRAY)
        self.needle_w = self.needle_img_gray.shape[1]
        self.needle_h = self.needle_img_gray.shape[0]

    def render_results(self):
        # Must draw in reverse order so that the most confident boxes are drawn on top.
        for box in reversed(self.result_boxes):
            # Colors are BGR
            if box.confidence >= .9:
                color = (0, 255, 0)  # Green
            elif box.confidence >= .8:
                color = (0, 255, 128)  # Light green
            elif box.confidence >= .7:
                color = (0, 255, 255)  # Yellow
            elif box.confidence >= .6:
                color = (0, 128, 255)  # Orange
            else:
                color = (0, 0, 255)  # Red
            cv2.rectangle(self.screenshot_rgb, (box.x, box.y), (box.x + box.width, box.y + box.height), color, 1)
            # print(f"Matching box at ({box.x}, {box.y}) with confidence level: {box.confidence}")

    def _search(self):  # sourcery skip: raise-specific-error
        if self.screenshot_gray is None:
            raise Exception("Screenshot not captured")
        if self.needle_img_gray is None:
            raise Exception("Needle not loaded")
        if self.USE_GRAYSCALE:
            match_template_result = cv2.matchTemplate(self.screenshot_gray, self.needle_img_gray, cv2.TM_CCOEFF_NORMED)
        else:
            match_template_result = cv2.matchTemplate(self.screenshot_rgb, self.needle_img_rgb, cv2.TM_CCOEFF_NORMED)

        match_locations = np.where(match_template_result >= self.MIN_CONFIDENCE)

        for (y, x) in zip(match_locations[0], match_locations[1]):
            confidence = match_template_result[y, x]
            self.result_boxes.append(ResultBox(x, y, self.needle_w, self.needle_h, confidence))

        self.result_boxes = sorted(self.result_boxes, key=lambda b: b.confidence, reverse=True)

    def best_confidence(self) -> float:
        return self.result_boxes[0].confidence if len(self.result_boxes) > 0.0 else 0.0

    def best_confidence_int(self) -> int:
        return round(self.best_confidence() * 100)

    def is_above_threshold(self) -> bool:
        return self.best_confidence() >= self.threshold

    def screeze_box(self) -> pyscreeze.Box:
        return pyscreeze.Box(self.result_boxes[0].x, self.result_boxes[0].y, self.needle_w, self.needle_h)

    def click_result(self):
        self.raise_if_not_found()
        image_center = pyautogui.center(self.screeze_box())
        logging.debug(f"Clicking at {image_center}")
        pyautogui.click(image_center)
        time.sleep(1.5)  # Wait for animations to finish.

    def search_and_click(self, max_seconds: float = 6):
        self.search_for(max_seconds)
        self.click_result()

    def search_for(self, max_seconds: float = 6) -> bool:
        start = time.time()
        while time.time() - start < max_seconds:
            self.capture_screen()
            self._search()
            if self.is_above_threshold():
                logging.info(f"Found '{self.needle_img_name}' "
                             f"with confidence {self.best_confidence_int()} "
                             f"in {round(time.time() - start, ndigits=2)} seconds")
                if debug_save_screen_images:
                    self.save_screen_to_file("found")
                return True
            time.sleep(min(1.0, max(0.1, max_seconds / 20.0)))
        logging.info(f"Could not find '{self.needle_img_name}' "
                     f"above confidence {self.threshold} "
                     f"within {round(time.time() - start, ndigits=2)} seconds "
                     f"found something @{self.best_confidence_int()}")
        if debug_save_screen_images:
            self.save_screen_to_file("nope")
        return False

    def raise_if_not_found(self):
        if not self.is_above_threshold():
            self.render_results()
            self.save_screen_to_file("missing")
            raise ImageNotFound("Image not found", self.needle_img_name)


class ResultBox:
    def __init__(self, x, y, width, height, confidence):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.confidence = confidence
