import time

import pyautogui

from as9.nav.navigation import ensure_touch_drive
from as9.util.game_images import *
from as9.util.utils import repeat_nitro


def lose_race():
    img_play_button.search_and_click()
    # click on the first car.
    time.sleep(2)
    # 900 is top car. 1600 the bottom
    pyautogui.click(800, 900)
    time.sleep(2)
    img_play_race.search_and_click()
    time.sleep(30)
    pyautogui.press('esc')
    img_quit_race.search_and_click(max_seconds=10)
