
class Anchor:
    def __init__(self, rope_length: float = 50):
        self.rope_length = rope_length
        self.is_dropped = False  # Якорь брошен?
        self.current_depth = 0.0  # Текущая глубина (если брошен)

    def drop(self, depth: float) -> bool:
        '''Опустить якорь'''
        if self.is_dropped:
            raise ValueError("Якорь уже брошен")
        if depth > self.rope_length:
            return False  # Канат слишком короткий
        self.is_dropped = True
        self.current_depth = depth
        return True

    def lift(self) -> None:
        '''Поднять якорь'''
        if not self.is_dropped:
            raise ValueError("Якорь уже поднят")

        self.is_dropped = False
        self.current_depth = 0.0
