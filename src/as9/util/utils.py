import logging
from typing import Optional

import pyautogui
import time

from pyscreeze import Box

from as9.util.constant import CAPTURE_DIR
from as9.util.constant import IMG_DIR


def scroll_horizontal(right=True):
    screen_width, screen_height = pyautogui.size()
    start_ratio = .9 if right else .1
    pyautogui.moveTo(x=int(screen_width * start_ratio), y=int(screen_height * .7))

    pyautogui.mouseDown()

    offset = int(screen_width * .75)
    if right:
        offset *= -1
    pyautogui.moveRel(xOffset=offset, yOffset=0, duration=1)

    pyautogui.mouseUp()


def sleep(time_sec=3, msg=''):
    logging.debug(f'Sleeping for {time_sec} seconds. {msg}')
    sleep_stage_sec = 5 * 60
    if time_sec < sleep_stage_sec:
        time.sleep(time_sec)
    else:
        while time_sec > 0:
            click_image('chat-open')
            click_image('chat-close')
            time.sleep(min(time_sec, sleep_stage_sec))
            time_sec -= sleep_stage_sec


def repeat_nitro(time_sec, nitro_every_sec=5):
    logging.debug("Starting nitro repeat...")
    start_time = time.time()
    while time.time() - start_time < time_sec:
        pyautogui.press('space')
        time.sleep(min(max(.5, time_sec - (time.time() - start_time)), nitro_every_sec))
    logging.debug("Finished nitro repeat.")


def find_image(image: str, min_conf: float = 0.5) -> (Optional[Box], float):
    logging.debug(f"Looking for {image}...")
    # Move mouse out of the way.
    # pyautogui.moveTo(1, 1)
    # find the highest confidence level of the image
    conf = .85
    while conf >= (min_conf - .01):
        image_location = pyautogui.locateOnScreen(f'{IMG_DIR}/{image}.png', confidence=conf, grayscale=True)
        if image_location:
            logging.debug(f"Found with confidence {round(conf, ndigits=2)} at {image_location}")
            # take screenshot of the image
            pyautogui.screenshot(f"{CAPTURE_DIR}/found-{image}.png", region=image_location)
            return image_location, conf
        conf -= .05
    logging.debug(f"Image not found at confidence {min_conf}")
    return None, 0


def wait_for_image(image: str, confidence: float = 0.7, timeout_sec: int = 30):
    logging.info(f"Waiting for {image}")
    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        if pyautogui.locateOnScreen(f'{IMG_DIR}/{image}.png', confidence=confidence):
            return True
        time.sleep(min(timeout_sec / 5, 1))
    raise ImageNotFound("Could not find image", image)


def click_image(image: str, min_conf: float = 0.4):
    image_location, _ = find_image(image, min_conf)
    if not image_location:
        raise ImageNotFound("Could not find image", image)
    click_box(image_location)


def click_image_if_exists(image: str, min_conf: float = 0.6) -> bool:
    image_location, _ = find_image(image, min_conf)
    if image_location:
        click_box(image_location)
        return True
    return False


def click_box(location: Box, sleep_sec: int = 2):
    image_center = pyautogui.center(location)
    logging.info(f"Clicking at {image_center}")
    pyautogui.click(image_center)
    time.sleep(sleep_sec)


class ImageNotFound(Exception):
    def __init__(self, message, image):
        self.message = message
        self.image = image
        pyautogui.screenshot(f"{CAPTURE_DIR}/not-found-{image}.png")
