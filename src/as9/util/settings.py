import logging


def current_hunt():
    """ Set what car hunt to run. """
    import as9.nav.hunts as hunts
    return hunts.AstonMartinOne77()


# 20 minutes, or 8 minutes with daily events bonus pass.
hunt_ticket_wait_min = 8

use_free_ticket_refill = True

hunt_d_cars = [
    'bp/ds-e-tense',
    'bp/elise-220',
    'bp/furai',
]
hunt_c_cars = [
    'bp/2017-nsx',
    'bp/h2',
    'bp/599',
    'bp/viper-acr',
    'bp/eb110',
]
hunt_b_cars = [
    'bp/asterion',
    'car/ap0',
    'bp/grand-sport',
    # 'bp/f12tdf',
    'car/elva',
    'bp/003s',
    'bp/488-gtb',

    # 'bp/berlinetta',
    # 'car/revuelto',
]

""" Main logging level. """
logging_level = logging.INFO

""" How long to pause on launch, before starting to perform actions."""
start_pause_sec = 4

debug_save_ocr_images = False
debug_save_screen_images = True

# Constants.
IMG_DIR = '../../../game-imgs'
CAPTURE_DIR = '../../../captures'
