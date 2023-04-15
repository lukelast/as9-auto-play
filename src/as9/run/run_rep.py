import logging

import as9.nav.navigation as nav
from as9.race.plan.scotland import ancient_ruins
from as9.race.race_runner import run_race
from as9.util.game_images import img_daily_events, img_legend_showcase, img_race_button, img_skip_button, \
    img_play0_button, img_refill_tickets, img_close_button
from as9.util.log import log_config
from as9.util.settings import start_pause_sec
from as9.util.utils import ImageNotFound, scroll_horizontal
from as9.util.utils import sleep

log_config()


def nav_to_race():
    nav.main_menu()
    img_daily_events.search_for()
    # Click twice to get into the events.
    img_daily_events.click_result()
    img_daily_events.click_result()

    img_legend_showcase.search_for(max_seconds=2)
    if not img_legend_showcase.is_above_threshold():
        scroll_horizontal(right=True)
        img_legend_showcase.search_for(max_seconds=2)
    if not img_legend_showcase.is_above_threshold():
        scroll_horizontal(right=False)
        img_legend_showcase.search_for(max_seconds=2)
    if not img_legend_showcase.is_above_threshold():
        scroll_horizontal(right=False)
        img_legend_showcase.search_for(max_seconds=2)

    img_legend_showcase.raise_if_not_found()

    # Must click twice to open the hunt page.
    img_legend_showcase.click_result()
    img_legend_showcase.click_result()


def loop_race():
    try:
        for _ in range(500):
            nav.open_free_pack()
            img_race_button.search_and_click()

            if img_skip_button.search_for(max_seconds=2):
                sleep(100 * 60, 'Waiting for gas')

            nav.ensure_touch_drive()
            img_play0_button.search_and_click()

            if img_refill_tickets.search_for(max_seconds=2):
                img_close_button.search_and_click()
                sleep(20 * 60, 'Waiting for tickets')
                img_play0_button.search_and_click()

            sleep(10, "loading race")

            run_race(ancient_ruins)

            nav.finish_race()

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
