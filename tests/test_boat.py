from decimal import Decimal

from app.constants import MAX_WEIGHT
from app.boat import Direction
from app.boat import Boat

import pytest


@pytest.fixture
def boat():
    """Фикстура, создающая экземпляр Boat для тестирования."""
    return Boat(weight=150.0)


def test_boat_initial_state(boat):
    assert boat.speed == 0.0
    assert boat.position == (Decimal('0.0'), Decimal('0.0'))
    assert boat._direction_vector == (0, 0)


def test_boat_movement(boat):
    # Опускаем весла
    boat.toggle_oars(dip=True)

    # Движение вверх
    status = boat.movement(Direction.UP)
    assert status["direction"] == Direction.UP.value
    assert status["speed"] > 0
    assert status["position"][1] < Decimal('0.0')


def test_weight_management(boat):
    # Проверка добавления веса
    assert boat.add_weight(MAX_WEIGHT - boat.weight) is True

    # Проверка перевеса
    assert boat.add_weight(MAX_WEIGHT) == 'Перевес'

    # Проверка снятия веса
    assert boat.remove_weight(boat.weight/2) == 'Вес снят'
    assert boat.remove_weight(boat.weight*2) == 'Вы пытаетесь снять больше чем есть в лодке'

    # Test that ValueError is raised with negative weight
    with pytest.raises(ValueError) as exc_info:
        boat.add_weight(-5)
    assert str(exc_info.value) == 'Вес отрицательный'
    assert exc_info.type is ValueError
