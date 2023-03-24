import logging
import time

import pyautogui

from as9.util.utils import click_box
from as9.util.utils import click_image
from as9.util.utils import click_image_if_exists
from as9.util.utils import find_image
from as9.util.utils import sleep


def ensure_touch_drive():
    logging.info("Checking touch drive status.")
    on_loc, on_conf = find_image('td-on', min_conf=0.4)
    off_loc, off_conf = find_image('td-off', min_conf=0.4)
    if off_conf > on_conf:
        logging.info("Touch drive is off. Turning on.")
        click_box(off_loc)


def open_free_pack():
    logging.info("Looking for free back button at the top of the screen.")
    free_pack_loc, _ = find_image('free-pack', min_conf=0.6)
    if not free_pack_loc:
        logging.info("Free pack not available")
        return
    pyautogui.click(pyautogui.center(free_pack_loc))
    click_image('open-free-pack')
    click_image('free-button')
    sleep(5)
    click_image('grey-next-button')
    click_image('back-button')


def to_main_menu():
    logging.info("Going home.")
    # Make sure focus is on the game window.
    pyautogui.click(1, 1)
    for _ in range(8):
        pyautogui.press('esc')
        time.sleep(1)
    if find_image('exit-game')[0]:
        pyautogui.press('esc')
    time.sleep(2)
    click_image_if_exists('legend-pass', min_conf=0.75)
