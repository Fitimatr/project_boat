import pytest
from app.boat import Boat


@pytest.fixture
def empty_boat():
    return Boat()
