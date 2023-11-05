from as9.clash.clash import ClashReader
from as9.util.log import log_config
from as9.util.settings import start_pause_sec
from as9.util.utils import sleep

log_config()


if __name__ == '__main__':
    sleep(start_pause_sec / 4, "starting")
    clash = ClashReader("20230911")
    clash.find_hoods()
