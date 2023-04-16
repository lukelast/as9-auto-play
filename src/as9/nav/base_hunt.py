import logging
import re
import time
from typing import Optional

import pyautogui

from as9.nav.navigation import ensure_touch_drive, select_car, finish_race
from as9.nav.navigation import open_free_pack
from as9.nav.navigation import main_menu
from as9.util.game_images import *
from as9.util.screen_img import ScreenImg
from as9.util.settings import hunt_ticket_wait_min
from as9.util.utils import ImageNotFound
from as9.util.utils import repeat_nitro
from as9.util.utils import scroll_horizontal
from as9.util.utils import sleep


class Hunt:

    def __init__(self):
        self.ticket_refill_minutes = hunt_ticket_wait_min
        # 12 minutes for D with multiplayer pass. 15 minutes for D.
        self.wait_for_gas_minutes = 20
        self.hunt_index = 0

        # The image name of the car to use.
        self.car1_img_name = 'car-elise-220'

        # The image name of the daily event.
        self.hunt = self.__class__.__name__
        self.car2_img: Optional[ScreenImg] = None

        self.config()

        self.img_hunt_event = ScreenImg(f"hunt/{self.hunt}", threshold=0.6)
        self.car1_img = ScreenImg(self.car1_img_name, threshold=0.7)

    def config(self):
        pass

    def single_hunt(self):
        """Run the hunt"""
        self.hunt_index += 1
        logging.info(f"Starting hunt {self.hunt_index}")
        self.start_race()
        # Sleep through the loading screen.
        # But never sleep past the start or else OCR will get behind.
        sleep(10)
        self.manage_race()
        finish_race()

    def manage_race(self):
        """Perform actions during the actual race."""
        repeat_nitro(45)

    def nav_to_hunt(self):
        main_menu()
        img_daily_events.search_for()
        # Click twice to get into the events.
        img_daily_events.click_result()
        img_daily_events.click_result()

        self.img_hunt_event.search_for(max_seconds=2)
        if not self.img_hunt_event.is_above_threshold():
            scroll_horizontal(right=True)
            self.img_hunt_event.search_for(max_seconds=2)
        if not self.img_hunt_event.is_above_threshold():
            scroll_horizontal(right=True)
            self.img_hunt_event.search_for(max_seconds=2)
        if not self.img_hunt_event.is_above_threshold():
            scroll_horizontal(right=False)
            self.img_hunt_event.search_for(max_seconds=2)
        if not self.img_hunt_event.is_above_threshold():
            scroll_horizontal(right=False)
            self.img_hunt_event.search_for(max_seconds=2)

        self.img_hunt_event.raise_if_not_found()

        # Must click twice to open the hunt page.
        self.img_hunt_event.click_result()
        self.img_hunt_event.click_result()

    def loop_hunt(self):
        try:
            for _ in range(500):
                open_free_pack()
                self.single_hunt()
        except ImageNotFound:
            logging.exception('Error in hunt.')

    def start_race(self):
        img_race_button.search_and_click()
        sleep(2, "List of cars has long scroll animation")
        select_car(self.car1_img)

        if img_skip_button.search_for(max_seconds=2):
            if self.car2_img is None:
                sleep(self.wait_for_gas_minutes * 60, 'Waiting for gas (no other car)')
            else:
                pyautogui.press('esc')
                select_car(self.car2_img)
                if img_skip_button.search_for(max_seconds=2):
                    sleep(self.wait_for_gas_minutes * 60, 'Waiting for gas')

        if self.hunt_index <= 2:
            ensure_touch_drive()

        img_play0_button.search_and_click()

        if img_refill_tickets.search_for(max_seconds=2):
            img_close_button.search_and_click()
            sleep(self.ticket_refill_minutes * 60, 'Waiting for tickets')
            img_play0_button.search_and_click()
