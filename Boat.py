MAX_WEIGHT = 200
WAVE_HEIGHT = 0.1
WIND_SPEED = 0.0


class Veslo:
    def __init__(self, side: str):
        self.side = side
        self.is_in_water = False

    def dip(self) -> None:
        self.is_in_water = True

    def lift(self) -> None:
        self.is_in_water = False


class Environment:
    def __init__(self):
        self.wave_height = 0.0  # waves height
        self.wind_speed = 0.0  # mps

    def update(self, wave_height: float, wind_speed: float) -> None:
        '''Обновление условий окружающей среды'''
        self.wave_height = wave_height
        self.wind_speed = wind_speed


class Boat:
    def __init__(self):
        self.weight = MAX_WEIGHT
