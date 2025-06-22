import pytest
from app.anchor import Anchor


@pytest.fixture
def anchor():
    """Фикстура, создающая экземпляр Anchor для тестирования."""
    return Anchor(rope_length=40.0)


class TestAnchor:
    def test_drop_already_dropped_raises_error(self):
        anchor = Anchor()
        anchor.drop(10)  # First drop succeeds
        with pytest.raises(ValueError, match="Якорь уже брошен"):
            anchor.drop(20)  # Second drop should raise error

    def test_lift_already_lifted_raises_error(self):
        anchor = Anchor()
        with pytest.raises(ValueError, match="Якорь уже поднят"):
            anchor.lift()  # Lift when not dropped

    def test_successful_drop_and_lift(self):
        anchor = Anchor(rope_length=100)
        assert anchor.drop(50) is True
        assert anchor.is_dropped is True
        assert anchor.current_depth == 50

        anchor.lift()
        assert anchor.is_dropped is False
        assert anchor.current_depth == 0.0

    def test_drop_too_deep_returns_false(self):
        anchor = Anchor(rope_length=50)
        assert anchor.drop(60) is False
        assert anchor.is_dropped is False
