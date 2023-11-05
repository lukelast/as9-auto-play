import logging

import mss as mss
import pyscreeze

from as9.nav.navigation import select_car
from as9.race.race_runner import play_action
from as9.race.plan.buenos_aires import to_the_docks
from as9.util.log import log_config
from as9.race.race_progress import RaceProgress
from as9.util.needle_img import NeedleImg
from as9.util.timer import Timer
from as9.util.utils import sleep

log_config()

if __name__ == '__main__':
    select_car(NeedleImg('car-488-gtb'))
