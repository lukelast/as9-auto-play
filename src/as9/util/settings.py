import logging


def current_hunt():
    """ Set what car hunt to run. """
    from as9.nav.base_hunt import HuntNagari
    return HuntNagari()


start_pause_sec = 4
debug_save_ocr_images = True
logging_level = logging.INFO
