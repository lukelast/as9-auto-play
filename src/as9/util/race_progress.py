import logging
import time

import cv2
import easyocr
import numpy as np
import pyscreeze
from PIL import ImageGrab

from as9.util.constant import CAPTURE_DIR

# Initialize EasyOCR with English as the chosen language
reader = easyocr.Reader(['en'])


class RaceProgress:
    # For testing purposes, use a test image as the screenshot.
    use_test_image = False
    save_debug_file = False
    max_jump = 8

    def __init__(self):
        self.race_percent = 0
        self.last_raw_read = 0

    def read_change(self) -> list[int]:
        new_percent = self.read_race_percent()

        result = []

        if new_percent == 0 \
                and self.last_raw_read == 0 \
                and self.race_percent > 95:
            result = [-1]  # Race is over
        elif new_percent == self.race_percent:
            pass  # No change
        elif new_percent == 0 and self.race_percent > 0:
            logging.warning("Failed to read percent. Ignoring.")
        elif new_percent < self.race_percent:
            logging.warning(f"Got {new_percent} which is lower than {self.race_percent}")
        elif new_percent > self.race_percent >= new_percent - self.max_jump:
            increase = new_percent - self.race_percent
            result = list(range(self.race_percent + 1, self.race_percent + increase + 1))
            self.race_percent = new_percent
        else:
            logging.warning(f"Got {new_percent} but current is "
                            f"{self.race_percent}. Ignoring.")

        self.last_raw_read = new_percent
        # print all fields
        # logging.debug(f"{vars(self)}")
        return result

    def read_race_percent(self):
        start_time = time.time()
        # Take a screenshot of the defined region
        screenshot = pyscreeze.screenshot()
        screen_np = np.array(screenshot)
        if self.use_test_image:
            screen_np = cv2.imread(f"{CAPTURE_DIR}/race2.png")

        # crop screenshot
        left = 500
        top = 140
        width = 300
        height = 150
        screen_np_cropped = screen_np[top:top + height, left:left + width]

        # Convert the PIL Image to an OpenCV image (BGR format)
        screen_cropped_color = cv2.cvtColor(screen_np_cropped, cv2.COLOR_RGB2BGR)

        # Convert the image to grayscale
        screen_cropped_gray = cv2.cvtColor(screen_cropped_color, cv2.COLOR_BGR2GRAY)

        # Use EasyOCR to detect text in the grayscale image
        result = reader.readtext(screen_cropped_gray, detail=0)

        numbers = [''.join(char for char in item if char.isdigit()) for item in result]
        # filter out empty strings
        numbers = list(filter(None, numbers))

        number = int(numbers[0]) if len(numbers) == 1 else ''
        # if 3 digits, then the % was read as a number, so remove the last one
        if len(str(number)) == 3:
            number = str(number)[:-1]
        try:
            percent_found = int(number)
        except ValueError:
            percent_found = 0

        if self.save_debug_file:
            cv2.imwrite(f"{CAPTURE_DIR}/{int(time.time())}-race-percent-crop-{percent_found}.png",
                        screen_cropped_gray)

        logging.debug(f"read {percent_found} in {time.time() - start_time:.2f} seconds")

        return min(99, percent_found)
