import logging
import os
import time

import cv2
import easyocr
import mss
import numpy as np
import pyscreeze

from as9.util.constant import CAPTURE_DIR
from as9.util.settings import debug_save_ocr_images
from as9.util.timer import Timer

# Initialize EasyOCR with English as the chosen language
reader = easyocr.Reader(['en'])


def _find_progress_region():
    region = mss.mss().monitors[1]
    region['left'] = int(region['width'] * 0.13)
    region['top'] = int(region['height'] * 0.07)
    region['width'] = int(region['width'] * 0.08)
    region['height'] = int(region['height'] * 0.06)
    return region


class RaceProgress:
    """
    Continuously read the screen to find the percentage of the race
    that has been completed.
    Each new race percentage is only output once.
    """
    # If the next value increase the current by more than this,
    # then we assume an error and ignore it.
    # My main concern is that sometimes the % is read as 9.
    # So we could go from 1 to 19, so keep this small to avoid that.
    max_jump = 6

    def __init__(self):
        self.race_percent = 0
        self.last_raw_read = 0
        self.progress_region = _find_progress_region()

    def check_new_percent(self) -> list[int]:
        """
        :return: [-1] means the race is over.
                [] means no change.
                Normal response is a list containing 1 new percent value.
                If for some reason we climbed multiple percent since the last check,
                then the list will contain multiple values.
        """
        new_percent = self.read_race_percent()

        result = []

        if new_percent == 0 \
                and self.last_raw_read == 0 \
                and self.race_percent > 95:
            result = [-1]  # Race is over
        elif new_percent == self.race_percent:
            pass  # No change
        elif new_percent == 0 and self.race_percent > 0:
            logging.debug("Was unable to read race progress percent.")
        elif new_percent < self.race_percent:
            # After we hit 99 the screen animates, and we get garbage results.
            if self.race_percent != 99:
                logging.warning(f"Got {new_percent} which is lower than {self.race_percent}")
        elif new_percent > self.race_percent >= new_percent - self.max_jump:
            increase = new_percent - self.race_percent
            result = list(range(self.race_percent + 1, self.race_percent + increase + 1))
            self.race_percent = new_percent
        else:
            logging.warning(f"Got {new_percent} but current is "
                            f"{self.race_percent}. Ignoring.")

        self.last_raw_read = new_percent
        return result

    def read_race_percent(self):
        start_time = time.time()
        with Timer() as screenshot_timer:
            screenshot = self._screenshot_mss()
            # screenshot = self._screenshot()
            # screenshot = self._screenshot_from_img()

        with Timer() as ocr_timer:
            percent_found = self._do_ocr(screenshot)

        if debug_save_ocr_images:
            _dir = f"{CAPTURE_DIR}/ocr"
            if not os.path.exists(_dir):
                os.makedirs(_dir)
            cv2.imwrite(f"{_dir}/{int(time.time())}-race-percent-crop-{percent_found}.png",
                        screenshot)

        total_ms = int((time.time() - start_time) * 1000)
        logging.debug(f"read {percent_found} in {total_ms} ms, "
                      f"ocr took {ocr_timer()}, "
                      f"screenshot took {screenshot_timer()}.")

        return max(0, min(99, percent_found))

    def _do_ocr(self, screenshot) -> int:
        # Use EasyOCR to detect text in the grayscale image
        raw_result = reader.readtext(screenshot, detail=0)
        logging.debug(f"OCR result: {raw_result}")

        # % is read as 9
        # A 9 was read as g
        # Strange values that have been seen.
        # 198
        # 990

        words = [''.join(char for char in item if char.isdigit() or char == '%' or char == 'g')
                 for item in raw_result]
        # filter out empty strings
        words = list(filter(None, words))

        if not words:
            return 0

        if len(words) > 1:
            logging.warning(f"Got more than 1 word from OCR: {words}. Raw result: {raw_result}")
            return 0

        word = words[0]
        assert word
        if len(word) >= 4:
            logging.warning(f"too long: {word}. Raw result: {raw_result}")
            return 0
        # Assume any 'g' is a 9
        word = word.replace('g', '9')
        try:
            if len(word) == 1:
                # Not expected, maybe make this a warning and return 0?
                return int(word)
            elif len(word) == 2:
                first, second = word
                if second == '%':
                    return int(first)
                elif second == '9':
                    # We have 2 digits ending in 9, without a %.
                    # Most likely the % was read as 9.
                    return int(first)
                else:
                    return int(word)
            elif len(word) == 3:
                first, second, third = word
                if third == '%' or third == '9':
                    return int(f"{first}{second}")
        except ValueError:
            logging.warning(f"Got non-digit: {word}. Raw result: {raw_result}")
            return 0

        logging.warning(f"Got unexpected word: {word}. Raw result: {raw_result}")
        return 0

    def _screenshot(self):
        region = self.progress_region
        region_tuple = (region['left'], region['top'], region['width'], region['height'])
        screenshot = pyscreeze.screenshot(region=region_tuple)
        screen_np = np.array(screenshot)
        gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
        return gray

    def _screenshot_mss(self):
        with mss.mss() as sct:
            screenshot = sct.grab(self.progress_region)
        screenshot_np = np.array(screenshot)
        screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGRA2GRAY)
        return screenshot_gray

    def _screenshot_from_img(self):
        region = self.progress_region
        left = region['left']
        top = region['top']
        width = region['width']
        height = region['height']
        screen_np = cv2.imread(f"{CAPTURE_DIR}/race-4k.png")
        gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)
        gray_cropped = gray[top:top + height, left:left + width]
        return gray_cropped
