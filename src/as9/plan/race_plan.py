import logging

import pyautogui

from as9.util.race_progress import RaceProgress


def run_race(plan, slow_computer=False):
    progress = RaceProgress()
    if slow_computer:
        # Run actions sooner if computer is slow.
        plan = {progress - 1: action for progress, action in plan.items()}
    while True:
        result = progress.read_change()
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


meiji_rush = {
    7: 'right',
    10: 'nitro2',
    15: 'drift-start',
    25: 'drift-stop',
    29: 'nitro2',
    33: 'nitro-stop',
    34: 'nitro',
}

# Buenos Aires
to_the_docks = {
    # Initial left drift.
    3: 'drift-start',
    7: ('drift-stop', 'nitro2'),

    # Nitro bottle
    11: 'left',

    12: ('nitro-stop', 'nitro'),

    # Double nitro bottle
    24: 'right',

    37: 'drift-start',
    40: 'right',
    41: ('drift-stop', 'nitro2'),

    # Left drift into S route
    45: 'drift-start',
    47: 'left',
    50: 'drift-stop',
    # 51: 'nitro',

    # Left out of S
    56: 'drift-start',
    59: ('drift-stop', 'nitro2'),

    # Slight right, see if we can skip the drift.
    62: 'nitro-stop',
    63: 'nitro',
    # 65: 'drift-start',
    # 67: 'drift-stop',
    # 68: 'nitro2',

    # Super sharp left corner
    68: 'drift-start',
    72: ('drift-stop', 'nitro2'),

    # Slight right corner
    77: 'drift-start',
    80: ('drift-stop', 'nitro2'),

    # Final left corner
    83: 'drift-start',
    86: ('drift-stop', 'nitro2'),

}
