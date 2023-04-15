import logging
import time

from as9.race.race_progress import RaceProgress
import pyautogui


def run_race(plan, slow_computer=False):
    progress = RaceProgress()
    if slow_computer:
        # Run actions sooner if computer is slow.
        plan = {progress - 1: action for progress, action in plan.items()}
    start = time.perf_counter()
    while time.perf_counter() - start < 300:
        result = progress.check_new_percent()
        if result == [-1]:
            logging.info("Race Over")
            break  # Race is over
        if not result:
            continue  # No new progress

        logging.debug(f"Perform actions on progress: {result}")
        for percent_step in result:
            action = plan.get(percent_step, None)
            if isinstance(action, tuple):
                for sub_action in action:
                    play_action(sub_action)
            elif action:
                play_action(action)


def play_action(action):
    logging.info(f"Perform action: {action}")
    if action == "nitro":
        pyautogui.press("space")
    elif action == "nitro2":
        pyautogui.press("space")
        pyautogui.press("space")
    elif action == "nitro-stop":
        pyautogui.keyDown("s")
        pyautogui.keyUp("s")

    elif action == "drift-start":
        pyautogui.keyDown("s")
    elif action == "drift-stop":
        pyautogui.keyUp("s")

    elif action == "left":
        pyautogui.press("a")
    elif action == "right":
        pyautogui.press("d")
