import logging
import pyautogui

from as9.nav.base_hunt import Hunt
from as9.race.plan.auckland import straight_sprint, side_view
from as9.race.plan.buenos_aires import to_the_docks, crosstown
from as9.race.plan.caribbean import islet_race
from as9.race.plan.himalayas import landslide
from as9.race.plan.nevada import hairpin_sprint
from as9.race.plan.osaka import rat_race
from as9.race.plan.paris import metro
from as9.race.race_runner import run_race
from as9.util.screen_img import ScreenImg
from as9.util.utils import sleep, repeat_nitro


class AstonMartinOne77(Hunt):
    def config(self):
        self.car_class = 'C'

    def manage_race(self):
        repeat_nitro(50)


class CorvetteC7R(Hunt):
    def manage_race(self):
        repeat_nitro(50)


class ApolloIE(Hunt):
    def config(self):
        self.car_class = 'C'

    def manage_race(self):
        """Perform actions during the actual race."""
        repeat_nitro(50)


class RenaultTrezor(Hunt):
    def manage_race(self):
        repeat_nitro(60)


class Bacalar(Hunt):
    pass


class NsxGt3Evo(Hunt):
    def manage_race(self):
        run_race(side_view)


class D8Gto(Hunt):
    pass


class GinettaG60(Hunt):
    pass


class ZondaHpBarchetta(Hunt):
    def config(self):
        self.car_class = 'B'

    def manage_race(self):
        run_race(straight_sprint)


class MclarenElva(Hunt):
    def config(self):
        self.car_class = 'C'

    def manage_race(self):
        run_race(crosstown)


class CorsaRrTurbo(Hunt):
    def manage_race(self):
        run_race(islet_race)


class ApexAp0(Hunt):
    def config(self):
        self.car_class = 'C'

    def manage_race(self):
        run_race(rat_race)


class PeugeotSr1(Hunt):
    pass


class FerrariMonzaSp1(Hunt):
    def manage_race(self):
        run_race(metro)


class NioEp9(Hunt):
    def config(self):
        self.car_class = 'B'

    def manage_race(self):
        run_race(hairpin_sprint)


class PorschePanameraTurboS(Hunt):
    pass


class mura(Hunt):
    def manage_race(self):
        repeat_nitro(44)


class FordGtMk2(Hunt):
    def config(self):
        self.car_class = 'C'

    def manage_race(self):
        repeat_nitro(60)


class ArashAf8FalconEdition(Hunt):
    def config(self):
        self.car_class = 'C'


class FerrariRoma(Hunt):
    def config(self):
        self.car_class = 'C'


class LotusEliseSprint220(Hunt):
    pass


class BugattiEb110(Hunt):
    def manage_race(self):
        """Perform actions during the actual race."""
        # repeat_nitro(50)
        run_race(metro)


class AstonMartinVictor(Hunt):
    def config(self):
        """
        The requirement is 44s
        488-gtb gets 42s using race plan.
        berlinetta gets 43.2s using basic nitro.
        asterion gets 42.3 using race plan.
        ap0 gets 39.4 using race plan. Which gets first.
        revuelto
        grand-sport
        """
        self.wait_for_gas_minutes = 40
        self.car_class = 'B'
        # self.car_img_names = ['car-488-gtb']

    def manage_race(self):
        run_race(to_the_docks)


class Porsche718CaymanGt4Clubsport(Hunt):
    pass


class BentleyContinentalGtSpeed(Hunt):
    def config(self):
        self.car_class = 'B'

    def manage_race(self):
        repeat_nitro(48)


class Porsche911Gt1Evolution(Hunt):
    def config(self):
        self.car_class = 'C'


class Hunt003s(Hunt):
    def config(self):
        self.hunt = 'hunt-scg-003s'
        self.car_class = 'C'

    def manage_race(self):
        # The NSX can just barely make it without a race plan.
        # super().manage_race()
        run_race(landslide)


class HuntNagari(Hunt):
    def config(self):
        self.hunt = 'hunt-nagari'

    def manage_race(self):
        run_race(to_the_docks)


class HuntGte(Hunt):
    def config(self):
        self.hunt = 'hunt-gte'
        self.car_class = 'C'


class HuntH2(Hunt):
    def config(self):
        self.hunt = 'hunt-h2'


class Hunt599xx(Hunt):
    def config(self):
        self.hunt = '599xx'


class HuntTaycan(Hunt):
    def config(self):
        self.hunt = 'hunt-taycan'

    def manage_race(self):
        sleep(4)
        logging.info('Orange Nitro')
        pyautogui.press('space')
        pyautogui.press('space')
        sleep(11)
        logging.info('Yellow Nitro')
        pyautogui.press('space')
        sleep(35)
