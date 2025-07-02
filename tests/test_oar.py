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


@pytest.mark.parametrize("side,expected_side,in_water,durability", [
    ('left', 'left', False, 100.0),
    ('right', 'right', False, 100.0),
])
def test_initialization(side, expected_side, in_water, durability):
    '''Тест инициализации весла'''
    oar = Oar(side=side)
    assert oar.side == expected_side
    assert oar.in_water == in_water
    assert oar.durability == durability


@pytest.mark.parametrize('oar_side', ['left', 'right'])
def test_dip_and_lift(oar_side):
    '''Тест опускания и поднятия весла'''
    oar = Oar(side=oar_side)
    oar.dip()
    assert oar.in_water, f'Весло {oar_side} должно быть в воде после dip()'
    oar.lift()
    assert not oar.in_water, (
        f'Весло {oar_side} не должно '
        f'быть в воде после lift()'
    )


@pytest.mark.parametrize('oar_side', ['left', 'right'])
def test_row_without_dipping(oar_side):
    '''Тест гребли без опускания весла в воду'''
    oar = Oar(side=oar_side)
    result = oar.row(10.0)
    assert result == 0.0, (
        f'Ожидалась нулевая сила гребка с поднятым веслом, получено {result}')


@pytest.mark.parametrize('oar_side', ['left', 'right'])
def test_row_with_dipping(oar_side):
    '''Тест гребли с опущенным веслом (одним)'''
    oar = Oar(side=oar_side)
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
