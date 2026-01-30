from .Usine import Usine
from .Client import Client


class Camion:
    def __init__(self, capacity: float, x: float, y: float, to_x: float = 0.0, to_y: float = 0.0, full: int = 20, empty : int = 10) -> None:
        self._capacity = 80.0 
        self.capacity = capacity

        self._state = True  # True = actif, False = à l'arret
        self._empty = empty
        self._full = full

        self._x = float(x)
        self._y = float(y)

        self._to_x = float(to_x)
        self._to_y = float(to_y)

        self._to_location: Client | Usine | None = None  # usine ou client ou None

    @property
    def capacity(self) -> float:
        return self._capacity

    @capacity.setter
    def capacity(self, value: float) -> None:
        value = float(value)
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
        self._state = bool(value)

    @property
    def empty(self) -> float:
        return self._empty

    @empty.setter
    def empty(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("empty ne peut pas être négatif.")
        if value + self._full > self._capacity:
            raise ValueError("Capacité camion dépassée (empty + full > capacity).")
        self._empty = value

    @property
    def full(self) -> float:
        return self._full

    @full.setter
    def full(self, value: float) -> None:
        value = float(value)
        if value < 0:
            raise ValueError("full ne peut pas être négatif.")
        if value + self._empty > self._capacity:
            raise ValueError("Capacité camion dépassée (empty + full > capacity).")
        self._full = value

    @property
    def load(self) -> float:
        return self._empty + self._full

    @property
    def free_space(self) -> float:
        return max(0.0, self._capacity - self.load)

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = float(value)

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = float(value)

    @property
    def to_x(self) -> float:
        return self._to_x

    @to_x.setter
    def to_x(self, value: float) -> None:
        self._to_x = float(value)

    @property
    def to_y(self) -> float:
        return self._to_y

    @to_y.setter
    def to_y(self, value: float) -> None:
        self._to_y = float(value)

    @property
    def to_location(self) -> Client | Usine | None:
        return self._to_location

    @to_location.setter
    def to_location(self, value: Client | Usine | None) -> None:
        self._to_location = value

    def set_destination(self, location: Client | Usine) -> None:
        self._to_location = location
        if isinstance(location, Usine):
            self._to_x, self._to_y = float(location.x), float(location.y)
        else:
            self._to_x, self._to_y = float(location.x), float(location.y)

    def distance_to_destination(self) -> float:
        dx = self._to_x - self._x
        dy = self._to_y - self._y
        return (dx * dx + dy * dy) ** 0.5

    def travel_time_hours(self, speed_kmh: float = 70.0) -> float:
        d = self.distance_to_destination()
        return d / float(speed_kmh)

    def arrive(self) -> None:
        self._x = self._to_x
        self._y = self._to_y

    def arrive_usine(self, usine: Usine, target_full: float = 50.0) -> bool:
        if self._empty > 0:
            usine.empty += self._empty
            self._empty = 0.0
        need = max(0.0, float(target_full) - self._full)
        take = min(need, float(usine.full))
        usine.full -= take
        self._full += take
        return self._full >= float(target_full)

    def arrive_client(self, client: Client) -> None:
        # place totale dispo chez client
        free_space_client = max(0.0, float(client.capacity) - (float(client.full) + float(client.empty)))

        deliver = min(self._full, free_space_client) # on depose les pleines
        self._full -= deliver
        client.full += deliver

        pick = min(float(client.empty), self.free_space) # on recupere les vides
        client.empty -= pick
        self._empty += pick