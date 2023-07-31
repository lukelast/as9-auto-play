import logging
import time

import pyautogui

from as9.nav.navigation import ensure_touch_drive, select_car, finish_race
from as9.nav.navigation import main_menu
from as9.nav.navigation import open_free_pack
from as9.util.game_images import *
from as9.util.screen_img import ScreenImg
from as9.util.settings import hunt_ticket_wait_min, use_free_ticket_refill, hunt_b_cars, hunt_c_cars, hunt_d_cars
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

        # Set the override the cars used.
        # When empty, the car_class is used.
        self.car_img_names: list[str] = []

        # Auto select the cars based on class. D is the default, so set to C or B.
        self.car_class = 'D'

        # The image name of the daily event.
        self.hunt = self.__class__.__name__

        # Ask the subclass to configure us.
        self.config()

        # If car class is set, then provide default cars.
        if not self.car_img_names:
            if self.car_class == 'D':
                self.car_img_names = hunt_d_cars
            elif self.car_class == 'C':
                self.car_img_names = hunt_c_cars
            elif self.car_class == 'B':
                self.car_img_names = hunt_b_cars

        self.img_hunt_event = ScreenImg(f"hunt/{self.hunt}", threshold=0.7)
        self.car_images = [ScreenImg(name, threshold=0.8) for name in self.car_img_names]

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

        img_ready_to_claim.search_for(max_seconds=2)

        if img_ready_to_claim.is_above_threshold():
            pyautogui.press('esc')
            time.sleep(2)

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
        # Loop through all the cars looking for one with gas.
        while True:
            sleep(2, "List of cars has long scroll animation")
            the_car = self.car_images[0]
            select_car(the_car)
            if img_skip_button.search_for(max_seconds=2):
                if len(self.car_images) == 1:
                    sleep(self.wait_for_gas_minutes * 60, 'Waiting for gas (no other car)')
                    break
                else:
                    # Go back to the car list.
                    pyautogui.press('esc')
                    # Remove car from list and put at the end.
                    self.car_images = self.car_images[1:] + [the_car]
            else:
                break

        if self.hunt_index <= 2:
            ensure_touch_drive()

        img_play0_button.search_and_click()

        if img_refill_tickets.search_for(max_seconds=2):
            if use_free_ticket_refill:
                img_ticket_free_refill.search_for()
                if img_ticket_free_refill.is_above_threshold():
                    img_ticket_free_refill.click_result()
                else:
                    sleep(self.ticket_refill_minutes * 60, 'Waiting for tickets')
                img_close_button.search_and_click()
            else:
                img_close_button.search_and_click()
                sleep(self.ticket_refill_minutes * 60, 'Waiting for tickets')
            img_play0_button.search_and_click()


class Car:
    """A car to use in a hunt."""

    def __init__(self, img_name: str):
        self.img_name = img_name
        self.img = ScreenImg(self.img_name, threshold=0.7)
