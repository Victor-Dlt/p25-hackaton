
class Usine:
    def __init__(self, x: float, y: float, production_rate: float, empty: int, full: int) -> None:
        self._x = x
        self._y = y
        self._production_rate = production_rate # par jour
        self._empty = empty
        self._full = full
    
    @property
    def x(self) -> float:
        return self._x
    
    @property
    def y(self) -> float:
        return self._y
    
    @property
    def production_rate(self) -> float:
        return self._production_rate
    
    @property
    def empty(self) -> int:
        return self._empty
    
    @property
    def full(self) -> int:
        return self._full
    
    @empty.setter
    def empty(self, value: int) -> None:
        if value < 0:
            raise ValueError("Le nombre de bouteilles vides ne peut pas être négatif.")
        
        self._empty = value
    
    @full.setter
    def full(self, value: int) -> None:
        if value < 0:
            raise ValueError("Le nombre de bouteilles pleines ne peut pas être négatif.")
        
        self._full = value
    
