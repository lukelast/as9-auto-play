import mss


class ScreenRegion:
    def __init__(self):
        #  Size of the monitor
        self.full_screen: dict[str, int] = mss.mss().monitors[1]
        self.region: dict[str, int] = mss.mss().monitors[1]

    def adjust_left(self, percent: float):
        self.region['left'] = int(self.full_screen['width'] * percent)

    def adjust_top(self, percent: float):
        self.region['top'] = int(self.full_screen['height'] * percent)

    def adjust_width(self, percent: float):
        self.region['width'] = int(self.full_screen['width'] * percent)

    def adjust_height(self, percent: float):
        self.region['height'] = int(self.full_screen['height'] * percent)

    def ocr_coordinates_to_click(self, coordinates: list[list[int]]) -> tuple[int, int]:
        left = coordinates[0][0] + self.region['left']
        top = coordinates[0][1] + self.region['top']
        return left, top
