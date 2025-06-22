class Oar:
    def __init__(self, side: str):
        self.side = side  # 'left' или 'right'
        self.in_water = False
        self.durability = 100.0

    def dip(self) -> None:
        self.in_water = True

    def lift(self) -> None:
        self.is_in_water = False

    def row(self, force: float) -> float:
        if not self.in_water or self.durability <= 0:
            return 0.0
        self.durability -= force * 0.01
        return force * (self.durability / 100)
