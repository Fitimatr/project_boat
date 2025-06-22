from decimal import Decimal
from enum import Enum

from anchor import Anchor
from constants import MAX_WEIGHT, BOAT_WEIGHT
from constants import MAX_SPEED, STRENGTH, ANCHOR_SPEED_DROP

from oar import Oar


class Direction(Enum):
    '''Направления движения'''
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Boat:
    def __init__(
        self,
        weight: float = 150,
    ):
        self.speed = 0.0
        self.position = (Decimal('0.0'), Decimal('0.0'))
        self.strength = STRENGTH
        self.anchor = Anchor(rope_length=50)
        self.left_oar = Oar('left')
        self.right_oar = Oar('right')
        self._direction_vector = (0, 0)
        self.status = {}
        self.weight = weight

    def movement(self, direction: Direction):
        if self.anchor.is_dropped:
            self.speed = max(0, self.speed - ANCHOR_SPEED_DROP)

        # Гребля: сила зависит от опущенных весел
        # Весла будут изнашиваться постепенно
        else:
            l_force = self.left_oar.row(1.0) if self.left_oar.in_water else 0.0
            r_force = self.right_oar.row(1.0) if self.right_oar.in_water else 0.0

            # Расчет ускорения (чем больше сила - тем быстрее разгон)
            force = Decimal(str(l_force + r_force))
            acceleration = force * Decimal(self.strength) / Decimal(
                self.weight + BOAT_WEIGHT)

            # Обновление скорости и направления
            self.speed = float(min(
                Decimal(MAX_SPEED),
                Decimal(self.speed) + acceleration
            ))
            self._direction_vector = direction.value

        dx = Decimal(self.speed * self._direction_vector[0])
        dy = Decimal(self.speed * self._direction_vector[1])

        self.position = (
            (self.position[0] + dx).quantize(Decimal('0.01')),
            (self.position[1] + dy).quantize(Decimal('0.01'))
        )

    def check_weight(self, additional_weight):
        if self.weight + additional_weight <= MAX_WEIGHT * 1.5:
            return True
        else:
            return False

    def add_weight(self, additional_weight):
        if self.check_weight(additional_weight):
            self.weight = self.weight + additional_weight
            return 'Вес успешно добавлен'
        else:
            return 'Перевес'

    def remove_weight(self, removed_weight: float):
        if removed_weight < 0:
            raise ValueError('Вес отрицательный')
        if removed_weight < self.weight:
            self.weight = Decimal(self.weight) - Decimal(removed_weight)
            return 'Вес снят'
        else:
            return 'Вы пытаетесь снять больше чем есть в лодке'

    def toggle_oars(self, dip: bool) -> None:
        '''Опустить/поднять оба весла.'''
        self.left_oar.dip() if dip else self.left_oar.lift()
        self.right_oar.dip() if dip else self.right_oar.lift()

    def get_status(self) -> dict:
        '''Возвращает текущее состояние лодки'''
        self.status = {
            "position": self.position,
            "speed": self.speed,
            "direction": self._direction_vector
        }
        return self.status


boat = Boat(weight=150.0)  # Лодка + гребец = 150 кг
boat.toggle_oars(dip=True)  # Опустить весла


print(boat.movement(Direction.UP))
