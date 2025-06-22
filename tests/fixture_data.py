import pytest
from app.anchor import Anchor
from app.oar import Oar


@pytest.fixture
def anchor():
    """Фикстура, создающая экземпляр Anchor для тестирования."""
    return Anchor(rope_length=40.0)


@pytest.fixture
def left_oar():
    """Фикстура для левого весла"""
    return Oar(side='left')


@pytest.fixture
def right_oar():
    """Фикстура для правого весла"""
    return Oar(side='right')


@pytest.fixture(params=['left', 'right'])
def any_oar(request):
    """Параметризованная фикстура для любого весла"""
    return Oar(side=request.param)
