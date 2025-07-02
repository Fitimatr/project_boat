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
    assert boat.speed == 0.0, 'Скорость лодки должна быть 0 при инициализации'
    assert boat.position == (Decimal('0.0'), Decimal('0.0')), (
        f'Начальная позиция должна быть (0, 0), получено {boat.position}'
    )
    assert boat._direction_vector == (0, 0), (
        'Начальный вектор направления должен быть (0, 0)'
    )


def test_boat_movement(boat):
    '''Движение лодки при опущенных веслах из начального положения'''
    boat.toggle_oars(dip=True)

    assert boat._direction_vector == (0, 0), (
        'Начальный вектор направления должен быть (0, 0)'
    )

    boat.toggle_oars(dip=True)
    boat.movement(Direction.UP)

    assert boat._direction_vector == Direction.UP.value, (
        f'После движения вверх вектор должен быть {Direction.UP.value}, '
        f'получено {boat._direction_vector}'
    )

    assert boat.speed > 0, 'Скорость должна увеличиться после движения'
    assert boat.position[1] < Decimal('0'), (
        f'Y-координата должна уменьшиться при движении вверх, '
        f'текущая позиция: {boat.position}'
    )


def test_weight_management(boat):
    '''Проверки на вес'''
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


def test_mass_movements(boat):
    '''Проверка на длительное перемещение в одну сторону'''
    initial_position = boat.position

    boat.left_oar.dip()
    boat.right_oar.dip()

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


@pytest.mark.parametrize('test_direction',
                         [Direction.DOWN, Direction.LEFT,
                          Direction.RIGHT, Direction.UP])
def test_movement_with_dropped_anchor(boat, test_direction):
    '''Тест движения лодки с брошенным якорем'''
    boat.anchor.drop(10)

    assert boat.anchor.is_dropped is True, 'Якорь должен быть брошен'
    initial_speed = boat.speed

    boat.movement(test_direction)

    assert boat.speed == max(0, initial_speed - ANCHOR_SPEED_DROP), (
        f'Скорость должна уменьшаться на 0.5 при брошенном якоре. '
        f'Ожидалось: {max(0, initial_speed - ANCHOR_SPEED_DROP)}, '
        f'Получено: {boat.speed}'
    )

    initial_speed = boat.speed


def test_direction_change(boat):
    '''Тест смены направления движения лодки'''
    boat.toggle_oars(dip=True)

    initial_position = boat.position

    boat.movement(Direction.UP)
    assert boat._direction_vector == Direction.UP.value, (
        f'Вектор направления должен быть {Direction.UP.value}, '
        f'получено {boat._direction_vector}'
    )
    assert boat.position[1] < initial_position[1], (
        f'При движении вверх Y должен уменьшаться. '
        f'Было: {initial_position[1]}, '
        f'стало: {boat.position[1]}'
    )
    up_position = boat.position

    boat.movement(Direction.DOWN)
    assert boat._direction_vector == Direction.DOWN.value, (
        f'Вектор направления должен быть {Direction.DOWN.value}, '
        f'получено {boat._direction_vector}'
    )
    assert boat.position[1] > up_position[1], (
        f'При движении вниз Y должен увеличиваться. '
        f'Было: {up_position[1]}, '
        f'стало: {boat.position[1]}'
    )
    down_position = boat.position

    boat.movement(Direction.LEFT)
    assert boat._direction_vector == Direction.LEFT.value, (
        f'Вектор направления должен быть {Direction.LEFT.value}, '
        f'получено {boat._direction_vector}'
    )
    assert boat.position[0] < down_position[0], (
        f'При движении влево X должен уменьшаться. '
        f'Было: {down_position[0]}, '
        f'стало: {boat.position[0]}'
    )
    left_position = boat.position

    boat.movement(Direction.RIGHT)
    assert boat._direction_vector == Direction.RIGHT.value, (
        f'Вектор направления должен быть {Direction.RIGHT.value}, '
        f'получено {boat._direction_vector}'
    )
    assert boat.position[0] > left_position[0], (
        f'При движении вправо X должен увеличиваться. '
        f'Было: {left_position[0]}, '
        f'стало: {boat.position[0]}'
    )
