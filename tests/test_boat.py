from decimal import Decimal

from app.constants import ANCHOR_SPEED_DROP, MAX_WEIGHT, MAX_SPEED
from app.boat import Direction
from app.boat import Boat

import pytest


@pytest.fixture
def boat():
    '''Фикстура, создающая экземпляр Boat для тестирования.'''
    return Boat(weight=150.0)


def test_boat_initial_state(boat):
    '''Изначальное состояние лодки'''
    boat = Boat()
    assert boat.speed == 0.0, 'Скорость лодки должна быть 0 при инициализации'
    assert boat.position == (Decimal('0.0'), Decimal('0.0')), (
        f'Начальная позиция должна быть (0, 0), получено {boat.position}'
    )
    assert boat._direction_vector == (0, 0), (
        'Начальный вектор направления должен быть (0, 0)'
    )


def test_boat_movement(boat):
    '''Движение лодки при опущенных веслах из начального положения'''
    boat = Boat()
    # Опускаем весла
    boat.toggle_oars(dip=True)

    # Движение вверх
    status = boat.movement(Direction.UP)
    assert status["direction"] == Direction.UP.value, (
        f'Направление должно быть {Direction.UP.value}, '
        f'получено {status['direction']}'
    )
    assert status["speed"] > 0, 'Скорость должна увеличиться при движении'
    assert status["position"][1] < Decimal('0.0'), (
        f'Y-координата должна уменьшаться при движении вверх, '
        f'получено {status['position'][1]}'
    )


def test_weight_management(boat):
    '''Проверки на вес'''
    boat = Boat()
    # Проверка добавления веса
    assert boat.add_weight(MAX_WEIGHT - boat.weight) == (
        'Вес успешно добавлен'
        ), (
        f'Должны были добавить {MAX_WEIGHT - boat.weight} веса'
    )

    # Проверка перевеса
    assert boat.add_weight(MAX_WEIGHT) == 'Перевес', (
        f'При весе {MAX_WEIGHT} должен быть перевес'
    )

    # Проверка снятия веса
    assert boat.remove_weight(boat.weight/2) == 'Вес снят', (
        'Должны были успешно снять половину веса'
    )
    assert boat.remove_weight(boat.weight*2) == (
        'Вы пытаетесь снять больше чем есть в лодке'), (
        'Не должны позволять снять больше веса чем есть'
    )


def test_mass_movements():
    '''Проверка на длительное перемещение в одну сторону'''
    boat = Boat()
    initial_position = boat.position

    # Убедимся, что лодка может двигаться:
    boat.left_oar.dip()  # Опускаем левое весло
    boat.right_oar.dip()  # Опускаем правое весло

    # Выполняем 1000 движений в одном направлении
    for _ in range(1000):
        boat.movement(Direction.UP)

    assert boat.speed <= MAX_SPEED, (
        f'Скорость {boat.speed} не должна превышать MAX_SPEED {MAX_SPEED}'
    )
    assert boat.position[1] != initial_position[1], (
        'Y-координата должна измениться после 1000 движений'
    )
    assert boat.position[0] == initial_position[0], (
        'X-координата не должна меняться при движении вверх'
    )
    assert boat.left_oar.durability < 100.0, (
        f'У левого весла должна снижаться прочность. '
        f'Нынешняя прочность {boat.left_oar.durability}'
    )
    assert boat.right_oar.durability < 100.0, (
        f'У правого весла должна снижаться прочность. '
        f'Нынешняя прочность {boat.right_oar.durability}'
    )


def test_movement_with_dropped_anchor():
    '''Тест движения лодки с брошенным якорем'''
    # Создаем лодку и бросаем якорь
    boat = Boat()
    boat.anchor.drop(10)  # Бросаем якорь на глубину 10

    # Проверяем начальное состояние
    assert boat.anchor.is_dropped is True, "Якорь должен быть брошен"
    initial_speed = boat.speed

    # Пытаемся двигаться в разных направлениях
    for direction in Direction:
        # Выполняем движение
        boat.movement(direction)

        # Проверяем что скорость уменьшилась
        assert boat.speed == max(0, initial_speed - ANCHOR_SPEED_DROP), (
            f'Скорость должна уменьшаться на 0.5 при брошенном якоре. '
            f'Ожидалось: {max(0, initial_speed - ANCHOR_SPEED_DROP)}, '
            f'Получено: {boat.speed}'
        )

        initial_speed = boat.speed  # Обновляем для следующей итерации
