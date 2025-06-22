
class Anchor:
    def __init__(self, rope_length: float):
        """
        :param rope_length: Длина якорного каната в метрах.
        """
        self.rope_length = rope_length
        self.is_dropped = False  # Якорь брошен?
        self.current_depth = 0.0  # Текущая глубина (если брошен)

    def drop(self, depth: float) -> bool:
        """Бросить якорь на заданную глубину.
        :return: True, если глубина <= длины каната.
        """
        if depth > self.rope_length:
            return False  # Канат слишком короткий
        self.is_dropped = True
        self.current_depth = depth
        return True

    def lift(self) -> None:
        """Поднять якорь."""
        self.is_dropped = False
        self.current_depth = 0.0
