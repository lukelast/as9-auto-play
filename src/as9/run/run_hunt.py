import logging


from as9.plan.base_hunt import Hunt
from as9.plan.base_hunt import Hunt599xx
from as9.plan.base_hunt import HuntGte
from as9.plan.base_hunt import HuntH2
from as9.plan.base_hunt import HuntTaycan
from as9.util.actions import to_main_menu
from as9.util.log import log_config
from as9.util.utils import ImageNotFound
from as9.util.utils import click_box
from as9.util.utils import find_image
from as9.util.utils import scroll_horizontal
from as9.util.utils import sleep

log_config()


def run_hunt(hunt: Hunt):
    to_main_menu()
    events_box = find_image('daily-events', 0.6)[0]
    if not events_box:
        raise ImageNotFound('Could not find daily events.', 'daily-events')
    # Click twice to get into the events.
    click_box(events_box)
    click_box(events_box)
    hunt_loc = find_image(hunt.hunt_image, 0.7)[0]
    if not hunt_loc:
        scroll_horizontal(right=True)
        hunt_loc = find_image(hunt.hunt_image, 0.7)[0]
    if not hunt_loc:
        scroll_horizontal(right=True)
        hunt_loc = find_image(hunt.hunt_image, 0.7)[0]
    if not hunt_loc:
        logging.error('Could not find the hunt.')
        raise ImageNotFound('Could not find the hunt.', hunt.hunt_image)

    # Must click twice to open the hunt page.
    click_box(hunt_loc)
    click_box(hunt_loc)
    hunt.run_hunt()


if __name__ == '__main__':
    sleep(5, "starting")
    for _ in range(100):
        try:
            run_hunt(HuntGte())
        except ImageNotFound:
            logging.exception('Error getting to hunt.')
            sleep(120, 'Waiting for error to resolve.')
