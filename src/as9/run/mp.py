from random import random

from as9.nav.mp import lose_race
from as9.nav.actions import open_free_pack
from as9.util.log import log_config

log_config()


if __name__ == '__main__':
    for _ in range(10):
        if random() < 0.2:
            open_free_pack()
        lose_race()

