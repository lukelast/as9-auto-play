import logging

from as9.util.log import log_config
from as9.util.settings import current_hunt
from as9.util.settings import start_pause_sec
from as9.util.utils import ImageNotFound
from as9.util.utils import sleep

log_config()

if __name__ == '__main__':
    sleep(start_pause_sec, "starting")
    hunt = current_hunt()
    for _ in range(100):
        try:
            hunt.nav_to_hunt()
            hunt.loop_hunt()
        except ImageNotFound:
            logging.exception('Error getting to hunt.')
            sleep(120, 'Waiting for error to resolve.')
