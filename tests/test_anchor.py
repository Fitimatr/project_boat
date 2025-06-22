import pytest
from app.anchor import Anchor


@pytest.fixture
def anchor():
    '''Фикстура, создающая экземпляр Anchor для тестирования.'''
    return Anchor(rope_length=40.0)


def test_drop_already_dropped_raises_error(anchor):
    anchor.drop(10)
    with pytest.raises(ValueError, match='Якорь уже брошен') as exc_info:
        anchor.drop(20)
    assert str(exc_info.value) == 'Якорь уже брошен', (
        'Должно быть сообщение "Якорь уже брошен"'
    )
    assert exc_info.type is ValueError, (
        'Должно вызываться исключение ValueError'
    )


def test_lift_already_lifted_raises_error(anchor):
    with pytest.raises(ValueError, match='Якорь уже поднят') as exc_info:
        anchor.lift()
    assert str(exc_info.value) == 'Якорь уже поднят', (
        'Должно быть сообщение "Якорь уже поднят"'
    )
    assert exc_info.type is ValueError, (
        'Должно вызываться исключение ValueError'
    )


def test_successful_drop_and_lift(anchor):
    anchor = Anchor(rope_length=100)
    assert anchor.drop(50) is True, (
        'Должны успешно бросить якорь на глубину 50'
    )
    assert anchor.is_dropped is True, (
        'Флаг is_dropped должен быть True после бросания, '
        'если глубина меньше длины веревки'
    )
    assert anchor.current_depth == 50, (
        f'Текущая глубина для якоря должна быть 50, '
        f'получено {anchor.current_depth}'
    )

    anchor.lift()
    assert anchor.is_dropped is False, (
        'Флаг is_dropped должен быть False после поднятия'
    )
    assert anchor.current_depth == 0.0, (
        f'Текущая глубина должна быть 0.0 после поднятия, '
        f'получено {anchor.current_depth}'
    )


def test_drop_too_deep_returns_false(anchor):
    anchor = Anchor(rope_length=50)
    assert anchor.drop(60) is False, (
        'Должны получить False при попытке бросить якорь глубже длины каната'
    )
    assert anchor.is_dropped is False, (
        'Флаг is_dropped должен остаться False при неудачной попытке'
    )
