import time

import pyautogui

from as9.util.utils import click_image
from as9.util.actions import ensure_touch_drive
from as9.util.utils import repeat_nitro
from as9.util.utils import sleep
from as9.util.utils import wait_for_image


def lose_race():
    click_image('play-button')
    # click on the first car.
    time.sleep(1)
    pyautogui.click(600, 600)
    ensure_touch_drive()
    click_image('play-button')
    repeat_nitro(120)
    wait_for_image('next-button', timeout_sec=120)
    click_image('next-button')
    click_image('next-button')
