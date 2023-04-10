import logging
import pyautogui
from as9.nav.base_hunt import Hunt
from as9.race.plan.buenos_aires import to_the_docks
from as9.race.plan.himalayas import landslide
from as9.race.race_runner import run_race
from as9.util.utils import sleep


class Hunt003s(Hunt):
    def __init__(self):
        super().__init__(hunt_image='hunt-scg-003s',
                         car_image='car-2017-nsx')

    def manage_race(self):
        # The NSX can just barely make it without a race plan.
        # super().manage_race()
        run_race(landslide)


class HuntNagari(Hunt):
    def __init__(self):
        super().__init__(hunt_image='hunt-nagari')

    def manage_race(self):
        run_race(to_the_docks)


class HuntGte(Hunt):
    def __init__(self):
        super().__init__(hunt_image='hunt-gte',
                         car_image='car-2017-nsx')


class HuntH2(Hunt):
    def __init__(self):
        super().__init__(hunt_image='hunt-h2')


class Hunt599xx(Hunt):
    def __init__(self):
        super().__init__(hunt_image='hunt-599xx')


class HuntTaycan(Hunt):
    def __init__(self):
        super().__init__(hunt_image='hunt-taycan')

    def manage_race(self):
        sleep(4)
        logging.info('Orange Nitro')
        pyautogui.press('space')
        pyautogui.press('space')
        sleep(11)
        logging.info('Yellow Nitro')
        pyautogui.press('space')
        sleep(35)
