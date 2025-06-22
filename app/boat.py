from enum import Enum
from decimal import Decimal

from anchor import Anchor
from oar import Oar

MAX_WEIGHT = 200
WAVE_HEIGHT = 0.0
WIND_SPEED = 0.0


class Environment:
    def __init__(self):
        self.wave_height = 0.0  # waves height
        self.wind_speed = 0.0  # mps

    def update(self, wave_height: float, wind_speed: float) -> None:
        '''Обновление условий окружающей среды'''
        self.wave_height = wave_height
        self.wind_speed = wind_speed


class Direction(Enum):
    """Направления движения"""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class Boat:
    def __init__(
        self,
        weight: float,
        max_speed: float = 5.0,
        stregth: float = 100
    ):
        self.weight = weight
        self.max_speed = max_speed
        self.speed = 0.0
        self.direction = 0.0
        self.position = (Decimal('0.0'), Decimal('0.0'))
        self.strength = stregth
        self.anchor = Anchor(rope_length=50)

    def movement(self, direction: Direction):
        if self.anchor.is_dropped:
            self.speed = max(0, self.speed - 0.5)
        else:
            self._direction_vector = direction.value
            acceleration = Decimal(self.strength) / Decimal(self.weight)

            self.speed = float(min(
                Decimal(self.max_speed),
                Decimal(self.speed) + acceleration
            ))

            dx = Decimal(self.speed * self._direction_vector[0])
            dy = Decimal(self.speed * self._direction_vector[1])

            self.position = (
                (self.position[0] + dx).quantize(Decimal('0.01')),
                (self.position[1] + dy).quantize(Decimal('0.01'))
            )

    def stop(self) -> None:
        """Постепенная остановка лодки"""
        self.speed = max(0, self.speed - 0.5)
        if self.speed < 0.1:
            self.speed = 0.0
            self._direction_vector = (0, 0)

    def get_status(self) -> dict:
        """Возвращает текущее состояние лодки"""
        return {
            "position": self.position,
            "speed": self.speed,
            "direction": self._direction_vector,
            "max_speed": self.max_speed,
            "strength": self.strength
        }


boat = Boat(weight=200)

# Движение вправо с интенсивностью 50%
boat.movement(Direction.RIGHT)
boat.movement(Direction.RIGHT)
boat.movement(Direction.RIGHT)
boat.movement(Direction.RIGHT)
boat.movement(Direction.RIGHT)
boat.movement(Direction.RIGHT)
print(f"Позиция: {boat.position[0]}; {boat.position[1]}. Скорость: {boat.speed:.1f}")

# Движение вниз с полной интенсивностью
boat.movement(Direction.DOWN)
boat.movement(Direction.DOWN)
boat.movement(Direction.DOWN)
boat.movement(Direction.DOWN)
print(f"Позиция: {boat.position[0]}; {boat.position[1]}. Скорость: {boat.speed:.1f}")
