from as9.util.log import log_config
from as9.util.screen_img import ScreenImg

log_config()

if __name__ == '__main__':

    img = ScreenImg(needle_img="test", threshold=0.8)
    img.search_for()
    img.save_screen_to_file()
    img.click_result()

    exit(0)


    start = time.time()
    for _ in range(10):
        find_image('my-career', 0.6)
    print(f"Duration: {time.time() - start} seconds")

    # click_image_if_exists('my-career', 0.65)

    # pyautogui.moveTo(x=1997, y=1886)
    # scroll_horizontal(right=False)
    # to_main_menu()
