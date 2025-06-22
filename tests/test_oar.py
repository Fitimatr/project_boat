import pytest
from app.oar import Oar


@pytest.fixture
def left_oar():
    '''Фикстура для левого весла'''
    return Oar(side='left')


@pytest.fixture
def right_oar():
    '''Фикстура для правого весла'''
    return Oar(side='right')


@pytest.fixture(params=['left', 'right'])
def any_oar(request):
    '''Параметризованная фикстура для любого весла'''
    return Oar(side=request.param)


def test_initialization():
    '''Тест инициализации весла'''
    left_oar = Oar(side='left')
    right_oar = Oar(side='right')

    assert left_oar.side == 'left', (
        f'Ожидалось side="left", получено {left_oar.side}')
    assert right_oar.side == 'right', (
        f'Ожидалось side="right", получено {right_oar.side}')
    assert not left_oar.in_water, (
        'Левое весло не должно быть в воде после инициализации')
    assert not right_oar.in_water, (
        'Правое весло не должно быть в воде после инициализации')
    assert left_oar.durability == 100.0, (
        f'Прочность левого весла должна быть 100%, '
        f'получено {left_oar.durability}')
    assert right_oar.durability == 100.0, (
        f'Прочность правого весла должна быть 100%, '
        f'получено {right_oar.durability}')


@pytest.mark.parametrize('side', ['left', 'right'])
def test_dip_and_lift(side):
    '''Тест опускания и поднятия весла'''
    oar = Oar(side=side)
    oar.dip()
    assert oar.in_water, f'Весло {side} должно быть в воде после dip()'
    oar.lift()
    assert not oar.in_water, f'Весло {side} не должно быть в воде после lift()'


@pytest.mark.parametrize('side', ['left', 'right'])
def test_row_without_dipping(side):
    '''Тест гребли без опускания весла в воду'''
    oar = Oar(side=side)
    result = oar.row(10.0)
    assert result == 0.0, (
        f'Ожидалась нулевая сила гребка с поднятым веслом, получено {result}')


@pytest.mark.parametrize('side', ['left', 'right'])
def test_row_with_dipping(side):
    '''Тест гребли с опущенным веслом'''
    oar = Oar(side=side)
    oar.dip()
    initial_durability = oar.durability
    force = 10.0

    result = oar.row(force)
    expected_result = force * (oar.durability / 100)

    assert result == expected_result, (
        f'Некорректная сила гребка. Ожидалось {expected_result}, '
        f'получено {result}'
    )
    assert oar.durability < initial_durability, (
        f'Прочность должна уменьшаться после гребка. '
        f'Было: {initial_durability}, стало: {oar.durability}'
    )
