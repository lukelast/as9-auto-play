import logging
import time

import pyautogui

from as9.util.game_images import *
from as9.util.utils import sleep, scroll_horizontal, ImageNotFound


def ensure_touch_drive():
    """Must be at the race screen where TD is enabled."""
    logging.info("Checking touch drive status.")
    # TODO just check for TD OFF with high confidence.
    img_td_on.search_for(max_seconds=1)
    img_td_off.search_for(max_seconds=1)
    if img_td_off.best_confidence_int() > img_td_on.best_confidence_int():
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


def main_menu():
    logging.info("Going home.")
    # Make sure focus is on the game window.
    pyautogui.click(1, 1)
    for _ in range(8):
        pyautogui.press('esc')
        time.sleep(1)
    if img_exit_game.search_for(max_seconds=2):
        time.sleep(1)
        pyautogui.press('esc')
    time.sleep(1)
    if img_legend_pass.search_for():
        img_legend_pass.click_result()


def select_car(car_img: ScreenImg):
    if car_img.search_for():
        car_img.click_result()
        return

    for _ in range(15):
        scroll_horizontal(right=False)

    for _ in range(25):
        if car_img.search_for(max_seconds=1):
            car_img.click_result()
            return
        scroll_horizontal(right=True)

    raise ImageNotFound(f"Trying to select car", car_img.needle_img_name)


def finish_race(skip_rewards: bool = False):
    """
    Click through the screens after a race is over.
    expect_rewards: Skip checking for rewards, to save time.
    """
    img_next_button.search_and_click(max_seconds=30)
    img_next_button.search_and_click()
    # Wait for the rewards animation to start, then press space to skip it.
    time.sleep(2)
    pyautogui.press('space')
    if img_gray_next_button.search_for(max_seconds=10):
        img_gray_next_button.click_result()
    else:
        logging.info("Did not give rewards.")
    logging.info('Finished Race')
