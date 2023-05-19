import logging


def current_hunt():
    """ Set what car hunt to run. """
    import as9.nav.hunts as hunts
    return hunts.FerrariRoma()


# 20 minutes, or 8 minutes with daily events bonus pass.
hunt_ticket_wait_min = 8

use_free_ticket_refill = True

""" Main logging level. """
logging_level = logging.INFO

""" How long to pause on launch, before starting to perform actions."""
start_pause_sec = 4

debug_save_ocr_images = False
debug_save_screen_images = True

# Constants.
IMG_DIR = '../../../game-imgs'
CAPTURE_DIR = '../../../captures'
