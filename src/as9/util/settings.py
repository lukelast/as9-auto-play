import logging


def current_hunt():
    """ Set what car hunt to run. """
    from as9.nav.base_hunt import HuntNagari
    return HuntNagari()


""" Main logging level. """
logging_level = logging.INFO

""" How long to pause on launch, before starting to perform actions."""
start_pause_sec = 4

debug_save_ocr_images = False
debug_save_screen_images = True


# Constants.
IMG_DIR = '../../../game-imgs'
CAPTURE_DIR = '../../../captures'
