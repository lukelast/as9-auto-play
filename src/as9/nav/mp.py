import time

import pyautogui

from as9.nav.navigation import ensure_touch_drive
from as9.util.game_images import *
from as9.util.utils import repeat_nitro


def lose_race():
    img_play_button.search_and_click()
    # click on the first car.
    time.sleep(1)
    pyautogui.click(600, 600)
    ensure_touch_drive()
    img_play_button.search_and_click()
    repeat_nitro(120)
    img_next_button.search_and_click(max_seconds=120)
    img_next_button.search_and_click()
