from decimal import Decimal

from app.constants import MAX_WEIGHT, MAX_SPEED
from app.boat import Direction
from app.boat import Boat

import pytest


@pytest.fixture
def boat():
    """Фикстура, создающая экземпляр Boat для тестирования."""
    return Boat(weight=150.0)


def test_boat_initial_state(boat):
    boat = Boat()
    assert boat.speed == 0.0
    assert boat.position == (Decimal('0.0'), Decimal('0.0'))
    assert boat._direction_vector == (0, 0)


def test_boat_movement(boat):
    boat = Boat()
    # Опускаем весла
    boat.toggle_oars(dip=True)

    # Движение вверх
    status = boat.movement(Direction.UP)
    assert status["direction"] == Direction.UP.value
    assert status["speed"] > 0
    assert status["position"][1] < Decimal('0.0')


def test_weight_management(boat):
    boat = Boat()
    # Проверка добавления веса
    assert boat.add_weight(MAX_WEIGHT - boat.weight) is True

    # Проверка перевеса
    assert boat.add_weight(MAX_WEIGHT) == 'Перевес'

    # Проверка снятия веса
    assert boat.remove_weight(boat.weight/2) == 'Вес снят'
    assert boat.remove_weight(boat.weight*2) == (
        'Вы пытаетесь снять больше чем есть в лодке')

    # Test that ValueError is raised with negative weight
    with pytest.raises(ValueError) as exc_info:
        boat.add_weight(-5)
    assert str(exc_info.value) == 'Вес отрицательный'
    assert exc_info.type is ValueError


def test_mass_movements():
    boat = Boat()
    initial_position = boat.position

    # Убедимся, что лодка может двигаться:
    boat.left_oar.dip()  # Опускаем левое весло
    boat.right_oar.dip()  # Опускаем правое весло

    # Выполняем 1000 движений в одном направлении
    for _ in range(1000):
        boat.movement(Direction.UP)

    assert boat.speed <= MAX_SPEED  # Не должна быть больше максимальной
    assert boat.position[1] != initial_position[1]  # Должны сместиться
    assert boat.position[0] == initial_position[0]  # X не менялся
