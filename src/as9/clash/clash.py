import dataclasses
import logging
import time
from dataclasses import dataclass
from typing import Optional

import easyocr
import pyautogui

from as9.util.needle_img import NeedleImg
from as9.util.screen_capture import ScreenCapture, save_jpg
from as9.util.screenshot import Screenshot
from as9.util.utils import scroll_horizontal


class ClashReader:
    def __init__(self, clash_date: str):
        self.clash_date = clash_date
        self.screen_capture = ScreenCapture(color=True)
        self.screen_capture.region.adjust_left(0.22)
        self.screen_capture.region.adjust_width(0.78)
        self.screen_capture.region.adjust_top(0.20)
        self.screen_capture.region.adjust_height(0.64)

        self.screen_street = ScreenCapture(color=True)
        self.screen_street.region.adjust_left(0.07)
        self.screen_street.region.adjust_width(0.86)
        self.screen_street.region.adjust_top(0.18)
        self.screen_street.region.adjust_height(0.64)

    def find_hoods(self):
        screen = ScreenCapture(color=True)
        image = screen.screenshot()
        result = image.do_ocr()
        image.draw_ocr(result)
        image.save("clash-debug", "ocr")
        for detection in result:
            coordinates, text, confidence = detection
            print(f"Coordinates: {coordinates}, Text: {text}, Confidence: {confidence:.2f}")

        for hood in hoods:
            if hood.ocr_text:
                for detection in result:
                    if hood.ocr_text.upper() == detection[1].upper():
                        click_loc = image.region.ocr_coordinates_to_click(detection[0])
                        logging.debug(f"Found {hood.name} using {detection[1]} with confidence {detection[2]}")
                        logging.debug(f"Clicking {click_loc}")
                        pyautogui.click(click_loc)
                        time.sleep(2)
                        self.capture_hood(hood.safe_name)
                        pyautogui.press('esc')
                        time.sleep(2)
                        break
            else:
                logging.debug(f"Hood {hood.name} has no ocr_text so using needle")

    def capture_hood(self, name: str):
        self.capture(name)
        logging.debug(f"Scrolling right for {name}")
        scroll_horizontal(right=True)
        scroll_horizontal(right=True)
        time.sleep(2)
        self.capture(name)

    def capture(self, name: str):
        logging.debug(f"Capturing {name}")
        screenshot: Screenshot = self.screen_capture.screenshot()
        result = screenshot.do_ocr()
        screenshot.draw_ocr(result)
        screenshot.save("clash-debug", "ocr")
        for detection in result:
            coordinates, text, confidence = detection
            print(f"Coordinates: {coordinates}, Text: {text}, Confidence: {confidence:.2f}")

        for detection in result:
            coordinates, text, confidence = detection
            if text == "0g":
                text = "09"
                logging.debug("Converted 0g to 09")
            if not (len(text) == 2 and text.isdigit()):
                logging.debug(f"Skipping '{text}'")
                continue
            if confidence < 0.8:
                logging.warning(f"'{text}' has low confidence {confidence}")

            click_position = screenshot.region.ocr_coordinates_to_click(coordinates)
            logging.debug(f"Clicking {click_position}")
            pyautogui.click(click_position)
            time.sleep(2)  # Animation
            race_img = self.screen_street.screenshot()
            race_img.save(f"clash-jpg/{self.clash_date}/{name}", text, timestamp=False, quality=20)
            race_img.save(f"clash-png/{self.clash_date}/{name}", text, timestamp=False, quality=100)

            # hit escape to close the window
            pyautogui.press('esc')
            time.sleep(2)  # Animation


@dataclass
class Hood:
    name: str
    ocr_text: str

    @property
    def safe_name(self) -> str:
        return self.name.replace(' ', '-')

    def needle_img(self) -> NeedleImg:
        return NeedleImg(f"clash/{self.safe_name}")


hoods = (
    Hood("gold hills", ""),
    Hood("the suburbs", "urbs"),
    Hood("back kitchen", ""),
    Hood("high village", "village"),
    Hood("the valley", "valley"),
    Hood("up town", "up town"),
    Hood("financial district", "financial"),
    Hood("river park", "park"),
    Hood("east valley", "east valley"),
    Hood("under pass", "under"),
)
