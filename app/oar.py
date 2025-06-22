class Oar:
    def __init__(self, side: str):
        self.side = side
        self.is_in_water = False

    def dip(self) -> None:
        '''Опустить весло в воду'''
        self.is_in_water = True

    def lift(self) -> None:
        '''Поднять весло из воды'''
        self.is_in_water = False
