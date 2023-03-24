import logging
import time
from random import random

import pyautogui

from as9.util.actions import ensure_touch_drive
from as9.util.actions import open_free_pack
from as9.util.utils import ImageNotFound
from as9.util.utils import click_image
from as9.util.utils import find_image
from as9.util.utils import repeat_nitro
from as9.util.utils import sleep
from as9.util.utils import wait_for_image


class Hunt:
    ticket_refill_minutes = 20
    wait_for_gas_minutes = 60
    hunt_image = ''
    car_image = ''

    def single_hunt(self, index: int):
        """Run the hunt"""
        raise NotImplementedError

    def run_hunt(self):
        try:
            for index in range(100):
                logging.info(f"Starting hunt {index}")
                if random() < 0.2:
                    open_free_pack()
                self.single_hunt(index)
        except ImageNotFound:
            logging.exception('Error in hunt.')

    def start_race(self, index: int):
        click_image('race-button')
        click_image(self.car_image)

        if find_image('skip-button', min_conf=0.7)[0]:
            sleep(self.wait_for_gas_minutes * 60, 'Waiting for gas')

        if index == 0:
            ensure_touch_drive()

        click_image('play0-button')

        if find_image('refill-tickets', min_conf=0.8)[0]:
            click_image('close-button')
            sleep(self.ticket_refill_minutes * 60, 'Waiting for tickets')
            click_image('play0-button')

    def collect_rewards(self):
        wait_for_image('next-button', timeout_sec=20)
        click_image('next-button')
        click_image('next-button')
        time.sleep(2)
        pyautogui.press('space')
        wait_for_image('grey-next-button', timeout_sec=10)
        click_image('grey-next-button')
        logging.debug('Finished round')


class HuntGte(Hunt):
    hunt_image = 'hunt-gte'
    car_image = 'car-2017-nsx'

    def single_hunt(self, index: int):
        self.start_race(index)
        sleep(12)
        repeat_nitro(45)
        self.collect_rewards()


class HuntH2(Hunt):
    hunt_image = 'hunt-h2'
    car_image = 'car-elise-220'

    def single_hunt(self, index: int):
        self.start_race(index)
        sleep(10)
        repeat_nitro(45)
        self.collect_rewards()


class Hunt599xx(Hunt):
    hunt_image = 'hunt-599xx'
    ticket_refill_minutes = 8
    wait_for_gas_minutes = 11
    car_image = 'car-elise-220'

    def single_hunt(self, index: int):
        self.start_race(index)
        sleep(10)
        repeat_nitro(45)
        self.collect_rewards()


class HuntTaycan(Hunt):
    hunt_image = 'hunt-taycan'
    car_image = 'car-elise-220'

    def single_hunt(self, index: int):
        self.start_race(index)

        sleep(16)
        logging.debug('Orange Nitro')
        pyautogui.press('space')
        pyautogui.press('space')
        sleep(11)
        logging.debug('Yellow Nitro')
        pyautogui.press('space')
        sleep(35)
        self.collect_rewards()


def grind():
    logging.info("Starting grind")
    click_image('race-button')
    # ensure_touch_drive()
    click_image('play0-button')
    repeat_nitro(110)
    wait_for_image('next-button', timeout_sec=60)
    click_image('next-button')
    click_image('next-button')
