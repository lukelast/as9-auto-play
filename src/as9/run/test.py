import logging
import string
import time

import cv2
import numpy as np
import pyautogui
from easyocr import easyocr
import pyscreeze

from as9.plan.race_plan import meiji_rush
from as9.plan.race_plan import play_action
from as9.plan.race_plan import to_the_docks
from as9.util.constant import CAPTURE_DIR
from as9.util.log import log_config
from as9.util.race_progress import RaceProgress
from as9.util.screen_img import ScreenImg
from as9.util.utils import sleep

log_config()

if __name__ == '__main__':
    sleep(2)

    progress = RaceProgress()
    plan = to_the_docks

    while True:
        result = progress.read_change()
        if result == [-1]:
            break  # Race is over
        elif result:
            logging.info(f"Perform actions on {result}")
            for percent_step in result:
                action = plan.get(percent_step, None)
                if isinstance(action, tuple):
                    for sub_action in action:
                        play_action(sub_action)
                elif action:
                    play_action(action)

    # pyautogui.screenshot(f"{CAPTURE_DIR}/race3.png")
    # logging.info("snapped")
