import logging
import time

import pyautogui

from as9.util.actions import ensure_touch_drive
from as9.util.actions import open_free_pack
from as9.util.actions import to_main_menu
from as9.util.game_images import *
from as9.util.screen_img import ScreenImg
from as9.util.utils import ImageNotFound
from as9.util.utils import repeat_nitro
from as9.util.utils import scroll_horizontal
from as9.util.utils import sleep


class Hunt:
    ticket_refill_minutes = 20
    wait_for_gas_minutes = 60

    def __init__(self, hunt_image: str, car_image: str = 'car-elise-220'):
        self.hunt_index = 0
        # The image name of the daily event.
        self.hunt_image = hunt_image
        # The image name of the car to use.
        self.car_image = car_image
        self.img_hunt = ScreenImg(self.hunt_image, threshold=0.6)
        self.img_car = ScreenImg(self.car_image, threshold=0.6)

    def single_hunt(self):
        """Run the hunt"""
        self.hunt_index += 1
        logging.info(f"Starting hunt {self.hunt_index}")
        self.start_race()
        sleep(12)
        self.manage_race()
        self.collect_rewards()

    def manage_race(self):
        """Perform actions during the actual race."""
        repeat_nitro(45)

    def nav_to_hunt(self):
        to_main_menu()
        img_daily_events.search_for()
        # Click twice to get into the events.
        img_daily_events.click_result()
        img_daily_events.click_result()

        self.img_hunt.search_for()
        if not self.img_hunt.is_above_threshold():
            scroll_horizontal(right=True)
            self.img_hunt.search_for()
        if not self.img_hunt.is_above_threshold():
            scroll_horizontal(right=True)
            self.img_hunt.search_for()
        if not self.img_hunt.is_above_threshold():
            scroll_horizontal(right=False)
            self.img_hunt.search_for()
        if not self.img_hunt.is_above_threshold():
            scroll_horizontal(right=False)
            self.img_hunt.search_for()

        self.img_hunt.raise_if_not_found()

        # Must click twice to open the hunt page.
        self.img_hunt.click_result()
        self.img_hunt.click_result()

    def loop_hunt(self):
        try:
            for _ in range(500):
                open_free_pack()
                self.single_hunt()
        except ImageNotFound:
            logging.exception('Error in hunt.')

    def start_race(self):
        img_race_button.search_and_click()
        self.img_car.search_and_click()

        if img_skip_button.search_for(max_seconds=2):
            sleep(self.wait_for_gas_minutes * 60, 'Waiting for gas')

        if self.hunt_index <= 1:
            ensure_touch_drive()

        img_play0_button.search_and_click()

        if img_refill_tickets.search_for(max_seconds=2):
            img_close_button.search_and_click()
            sleep(self.ticket_refill_minutes * 60, 'Waiting for tickets')
            img_play0_button.search_and_click()

    def collect_rewards(self):
        img_next_button.search_and_click(max_seconds=20)
        img_next_button.search_and_click()
        time.sleep(3)
        pyautogui.press('space')
        img_gray_next_button.search_and_click(max_seconds=20)
        logging.debug('Finished round')


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
        logging.debug('Orange Nitro')
        pyautogui.press('space')
        pyautogui.press('space')
        sleep(11)
        logging.debug('Yellow Nitro')
        pyautogui.press('space')
        sleep(35)
