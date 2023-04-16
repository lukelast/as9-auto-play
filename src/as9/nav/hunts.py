import logging
import pyautogui

from as9.nav.base_hunt import Hunt
from as9.race.plan.buenos_aires import to_the_docks
from as9.race.plan.himalayas import landslide
from as9.race.race_runner import run_race
from as9.util.screen_img import ScreenImg
from as9.util.utils import sleep, repeat_nitro


class BentleyContinentalGtSpeed(Hunt):
    def config(self):
        self.car1_img_name = 'car-488-gtb'
        self.car2_img = ScreenImg('car-asterion', threshold=0.7)

    def manage_race(self):
        repeat_nitro(48)


class Porsche911Gt1Evolution(Hunt):
    def config(self):
        self.car1_img_name = 'car-2017-nsx'
        self.wait_for_gas_minutes = 50


class Hunt003s(Hunt):
    def config(self):
        self.hunt = 'hunt-scg-003s'
        self.car1_img_name = 'car-2017-nsx'

    def manage_race(self):
        # The NSX can just barely make it without a race plan.
        # super().manage_race()
        run_race(landslide)


class HuntNagari(Hunt):
    def config(self):
        self.hunt = 'hunt-nagari'

    def manage_race(self):
        run_race(to_the_docks)


class HuntGte(Hunt):
    def config(self):
        self.hunt = 'hunt-gte'
        self.car1_img_name = 'car-2017-nsx'


class HuntH2(Hunt):
    def config(self):
        self.hunt = 'hunt-h2'


class Hunt599xx(Hunt):
    def config(self):
        self.hunt = '599xx'


class HuntTaycan(Hunt):
    def config(self):
        self.hunt = 'hunt-taycan'

    def manage_race(self):
        sleep(4)
        logging.info('Orange Nitro')
        pyautogui.press('space')
        pyautogui.press('space')
        sleep(11)
        logging.info('Yellow Nitro')
        pyautogui.press('space')
        sleep(35)
