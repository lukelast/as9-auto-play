import logging
import time

import pyautogui

from as9.util.game_images import *
from as9.util.utils import sleep


def ensure_touch_drive():
    logging.info("Checking touch drive status.")
    # TODO just check for TD OFF with high confidence.
    img_td_on.search_for(max_seconds=1)
    img_td_off.search_for(max_seconds=1)
    if img_td_off.best_confidence() > img_td_on.best_confidence():
        logging.info("Touch drive is off. Turning on.")
        img_td_off.click_result()


def open_free_pack():
    logging.info("Looking for free back button at the top of the screen.")
    img_free_pack.search_for(max_seconds=.5)
    if not img_free_pack.is_above_threshold():
        logging.info("Free pack not available")
        return
    img_free_pack.click_result()
    img_open_free_pack.search_and_click()
    img_free_button.search_and_click()
    sleep(5, "Cards displaying")
    img_gray_next_button.search_and_click()
    img_back_button.search_and_click()


def to_main_menu():
    logging.info("Going home.")
    # Make sure focus is on the game window.
    pyautogui.click(1, 1)
    for _ in range(8):
        pyautogui.press('esc')
        time.sleep(1)
    if img_exit_game.search_for(max_seconds=2):
        time.sleep(1)
        pyautogui.press('esc')
    time.sleep(2)
    if img_legend_pass.search_for():
        img_legend_pass.click_result()
