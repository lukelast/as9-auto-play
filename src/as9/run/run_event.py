import logging

import as9.nav.navigation as nav
from as9.race.plan.scotland import ancient_ruins
from as9.race.race_runner import run_race
from as9.util.game_images import img_daily_events, img_snapdragon1, img_race_button, img_skip_button, \
    img_play0_button, img_refill_tickets, img_close_button
from as9.util.log import log_config
from as9.util.settings import start_pause_sec
from as9.util.utils import ImageNotFound, scroll_horizontal, repeat_nitro
from as9.util.utils import sleep

log_config()


def nav_to_race():
    nav.main_menu()
    img_daily_events.search_for()
    # Click twice to get into the events.
    img_daily_events.click_result()
    img_daily_events.click_result()

    img_snapdragon1.search_for(max_seconds=2)
    if not img_snapdragon1.is_above_threshold():
        scroll_horizontal(right=True)
        img_snapdragon1.search_for(max_seconds=2)
    if not img_snapdragon1.is_above_threshold():
        scroll_horizontal(right=False)
        img_snapdragon1.search_for(max_seconds=2)
    if not img_snapdragon1.is_above_threshold():
        scroll_horizontal(right=False)
        img_snapdragon1.search_for(max_seconds=2)

    img_snapdragon1.raise_if_not_found()

    # Must click twice to open the hunt page.
    img_snapdragon1.click_result()
    img_snapdragon1.click_result()


def loop_race():
    try:
        for _ in range(500):
            nav.open_free_pack()
            img_race_button.search_and_click()

            nav.ensure_touch_drive()
            img_play0_button.search_and_click()

            sleep(10, "loading race")
            repeat_nitro(80)
            nav.finish_race(skip_rewards=True)

    except ImageNotFound:
        logging.exception('Error in hunt.')


if __name__ == '__main__':
    sleep(start_pause_sec, "starting")
    for _ in range(100):
        try:
            nav_to_race()
            loop_race()
        except ImageNotFound:
            logging.exception('Error getting to race.')
            sleep(120, 'Waiting for error to resolve.')
