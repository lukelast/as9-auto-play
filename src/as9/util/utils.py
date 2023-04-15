import logging
import time

import pyautogui
import pyscreeze

from as9.util.settings import CAPTURE_DIR


def scroll_horizontal(right=True):
    screen_width, screen_height = pyautogui.size()
    start_ratio = .9 if right else .1
    pyautogui.moveTo(x=int(screen_width * start_ratio), y=int(screen_height * .7))

    pyautogui.mouseDown()

    offset = int(screen_width * .75)
    if right:
        offset *= -1
    pyautogui.moveRel(xOffset=offset, yOffset=0, duration=0.5)

    pyautogui.mouseUp()


def sleep(time_sec=3, msg=''):
    logging.info(f'Sleeping for {time_sec} seconds. {msg}')
    # Ignore this for now and just let it disconnect.
    sleep_stage_sec = 999 * 60
    if time_sec < sleep_stage_sec:
        time.sleep(time_sec)
    else:
        from as9.util.screen_img import ScreenImg
        img_chat_close = ScreenImg('chat-close')
        img_chat_open = ScreenImg('chat-open')
        while time_sec > 0:
            img_chat_open.search_and_click()
            img_chat_close.search_and_click()
            time.sleep(min(time_sec, sleep_stage_sec))
            time_sec -= sleep_stage_sec


def repeat_nitro(time_sec, nitro_every_sec=5):
    logging.info("Starting nitro repeat...")
    start_time = time.time()
    while time.time() - start_time < time_sec:
        pyautogui.press('space')
        time.sleep(min(max(.5, time_sec - (time.time() - start_time)), nitro_every_sec))
    logging.info("Finished nitro repeat.")


class ImageNotFound(Exception):
    def __init__(self, message, image):
        self.message = message
        self.image = image
        pyscreeze.screenshot(f"{CAPTURE_DIR}/not-found-{image}.png")
