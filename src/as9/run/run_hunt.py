import logging

from as9.plan.base_hunt import HuntGte
from as9.util.log import log_config
from as9.util.utils import ImageNotFound
from as9.util.utils import sleep

log_config()


if __name__ == '__main__':
    sleep(10, "starting")
    for idx in range(100):
        try:
            hunt = HuntGte()
            hunt.nav_to_hunt()
            hunt.loop_hunt(idx)
        except ImageNotFound:
            logging.exception('Error getting to hunt.')
            sleep(120, 'Waiting for error to resolve.')
