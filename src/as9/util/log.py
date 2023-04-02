import logging
import sys
import os
import pyautogui
from as9.util.constant import CAPTURE_DIR


def log_config():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        stream=sys.stdout)
    if not os.path.exists(CAPTURE_DIR):
        os.makedirs(CAPTURE_DIR)
        os.makedirs(f"{CAPTURE_DIR}/ocr")
    pyautogui.screenshot(f"{CAPTURE_DIR}/start.png")
