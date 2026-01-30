
class Camion:
    def __init__(self, capacity: float) -> None:
        self._capacity = capacity
        self._state = False
        self._empty = 0
        self._full = 0
        self._next_action =


    @property
    def capacity(self) -> float:
        return self._capacity
    
    @capacity.setter
    def capacity(self, value: float) -> None:
        if value < 0:
            raise ValueError("La capacité doit être positive.")

        if value > 80:
            raise ValueError("La capacité ne peut pas dépasser 80 bouteilles.")

        self._capacity = value

    @property
    def state(self) -> bool:
        return self._state
    
    @state.setter
    def state(self, value: bool) -> None:
        self._state = value


