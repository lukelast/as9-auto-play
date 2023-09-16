from random import random

from as9.nav.mp import lose_race
from as9.nav.navigation import open_free_pack
from as9.util.log import log_config
from as9.util.settings import start_pause_sec
from as9.util.utils import sleep

log_config()


if __name__ == '__main__':
    sleep(start_pause_sec, "starting")
    for _ in range(10):
        open_free_pack()
        lose_race()

