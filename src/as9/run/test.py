import logging

import mss as mss
import pyscreeze

from as9.race.race_runner import play_action
from as9.race.plan.buenos_aires import to_the_docks
from as9.util.log import log_config
from as9.race.race_progress import RaceProgress
from as9.util.timer import Timer
from as9.util.utils import sleep

log_config()

if __name__ == '__main__':
    #sleep(2)

    race = RaceProgress()
    race.read_race_percent()

    exit()

    with mss.mss() as sct:
        # 0 is all screens
        monitor = sct.monitors[1]
        sct.grab(monitor)  # warmup grab.
        sct.grab(monitor)
        with Timer() as timer:
            # crop monitor
            monitor = {'left': 100, 'top': 100, 'width': 400, 'height': 200}
            screenshot = sct.grab(monitor)

        # Save the screenshot to a file
        mss.tools.to_png(screenshot.rgb, screenshot.size, output='screenshot.png')

    logging.info(f"sct took {timer()}")

    with Timer() as timer:
        pyscreeze.screenshot()
    logging.info(f"pyscreeze took {timer()}")

    # pyautogui.screenshot(f"{CAPTURE_DIR}/race3.png")
    # logging.info("snapped")
