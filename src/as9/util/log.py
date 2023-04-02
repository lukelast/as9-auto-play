import logging
import sys
import os
import pyautogui
from as9.util.constant import CAPTURE_DIR
from as9.util.settings import logging_level


def log_config():
    logging.basicConfig(level=logging_level,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        stream=sys.stdout)
    if not os.path.exists(CAPTURE_DIR):
        os.makedirs(CAPTURE_DIR)
        os.makedirs(f"{CAPTURE_DIR}/ocr")
    pyautogui.screenshot(f"{CAPTURE_DIR}/start.png")
