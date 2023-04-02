import logging


def current_hunt():
    """ Set what car hunt to run. """
    from as9.nav.base_hunt import HuntNagari
    return HuntNagari()

logging_level = logging.INFO
start_pause_sec = 4
debug_save_ocr_images = False
debug_save_screen_images = True

IMG_DIR = '../../../game-imgs'
CAPTURE_DIR = '../../../captures'
