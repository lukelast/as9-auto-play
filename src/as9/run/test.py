import logging
import sys
import time
from random import random

import pyautogui

from as9.util.actions import to_main_menu
from as9.util.log import log_config
from as9.util.utils import click_image_if_exists
from as9.util.utils import find_image

log_config()


if __name__ == '__main__':
    start = time.time()
    for _ in range(10):
        find_image('my-career', 0.6)
    print(f"Duration: {time.time() - start} seconds")

    #click_image_if_exists('my-career', 0.65)

    #pyautogui.moveTo(x=1997, y=1886)
    # scroll_horizontal(right=False)
    #to_main_menu()

