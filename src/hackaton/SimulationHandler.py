from typing import List, Tuple, Literal

from .Usine import Usine
from .Client import Client
from .Camion import Camion
from .utils import distance

EventType = Literal["ARRIVAL", "DEPART"]


class SimulationHandler:
    def __init__(
        self,
        camions: List[Camion],
        usine: Usine,
        clients: List[Client],
        speed_kmh: float = 70.0,
        target_full_at_plant: int = 50,
        price_per_full: float = 200,
        cost_per_km: float = 0.7,
    ) -> None:
        
        self._camions = camions
        self._usine = usine
        self._clients = clients

        self._speed_kmh = float(speed_kmh)
        self._target_full_at_plant = int(target_full_at_plant)

        self._price_per_full = float(price_per_full)
        self._cost_per_km = float(cost_per_km)

        self._revenue: float = 0.0
        self._travel_cost: float = 0.0

        self._events: List[Tuple[float, int, EventType]] = []
        self._current_time: float = 0.0

        self._production: float = 0.0
        self._consommation = [0.0 for _ in self._clients]

        for i in range(len(self._camions)):
            self.add_event(0.0, i, "ARRIVAL")


    @property
    def revenue(self) -> float:
        return self._revenue

    @property
    def travel_cost(self) -> float:
        return self._travel_cost

    @property
    def profit(self) -> float:
        return self._revenue - self._travel_cost

    def add_event(self, t: float, camion_idx: int, event_type: EventType) -> None:
        self._events.append((float(t), int(camion_idx), event_type))
        self._events.sort(key=lambda e: e[0])


    def _production_usine(self, dt_hours: float) -> None:
        if dt_hours <= 0:
            return

        prod_per_hour = float(self._usine.production_rate) / 24.0
        self._production += prod_per_hour * dt_hours

        produced_int = self._production
        if produced_int < 1:
            return

        produced_int = int(min(produced_int, int(self._usine.empty)))
        if produced_int <= 0:
            return

        self._production -= produced_int
        self._usine.empty = self._usine.empty - produced_int
        self._usine.full = self._usine.full + produced_int

    def _consommation_clients(self, dt_hours: float) -> None:
        if dt_hours <= 0:
            return

        for i, client in enumerate(self._clients):
            consumption_per_hour = client.consumption / 24
            self._consommation[i] += consumption_per_hour * dt_hours
            

            consumed = min(self._consommation[i], client.full)
            if consumed <= 0:
                continue

            self._consommation[i] -= consumed
            client.full = client.full - consumed
            client.empty = client.empty + consumed


    def _choose_next_destination(self, camion: Camion, exclude: Usine | Client | None) -> Usine | Client:
        if camion.empty > camion.full or camion.full <= 0:
            return self._usine

        best_client = None
        best_score = -1.0

        for client in self._clients:
            if client is exclude:
                continue

            d = distance(float(camion.x), float(camion.y), float(client.x), float(client.y))
            if d <= 0:
                continue 

            free_space = max(0.0, float(client.capacity) - (float(client.full) + float(client.empty)))
            n = min(free_space, float(camion.full))


            score = n / d

            if score > best_score:
                best_score = score
                best_client = client

        return best_client
        


    def _schedule_arrival(self, camion_idx: int, depart_time: float) -> None:
        camion = self._camions[camion_idx]

        d_km = distance(float(camion.x), float(camion.y), float(camion.to_x), float(camion.to_y))

        travel_h = d_km / self._speed_kmh if self._speed_kmh > 0 else 0.0
        next_time = depart_time + travel_h

        # Parce que notre programme boucle 
        if next_time <= depart_time + 1e-12:
            next_time = depart_time + 1e-6

        self.add_event(next_time, camion_idx, "ARRIVAL")

    def _schedule_depart(self, camion_idx: int, depart_time: float) -> None:
        if depart_time <= self._current_time + 1e-12:
            depart_time = self._current_time + 1e-6
        self.add_event(depart_time, camion_idx, "DEPART")


    def _process_arrival(self, camion_idx: int, t: float) -> None:
        camion = self._camions[camion_idx]

        # pas encore de destination
        if camion.to_location is None:
            dest = self._choose_next_destination(camion, exclude=None)
            camion.set_destination(dest)
            self._schedule_arrival(camion_idx, t)
            return

        # arrivée réelle
        camion.arrive()
        dest = camion.to_location

        if isinstance(dest, Usine):
            can_leave = camion.arrive_usine(self._usine, target_full=float(self._target_full_at_plant))
            if not can_leave:
                missing = max(0.0, float(self._target_full_at_plant) - float(camion.full))
                prod_per_hour = float(self._usine.production_rate) / 24.0
                if prod_per_hour <= 0:
                    camion.state = False
                    return
                wait_h = missing / prod_per_hour
                camion.state = False
                self._schedule_depart(camion_idx, t + wait_h)
                return

        else:
            free_space = max(0.0, float(dest.capacity) - (float(dest.full) + float(dest.empty)))
            delivered_full = int(min(float(camion.full), free_space))

            camion.arrive_client(dest)

            if self._price_per_full != 0.0 and delivered_full > 0:
                self._revenue += self._price_per_full * delivered_full

    
        next_dest = self._choose_next_destination(camion, exclude=dest)
        camion.set_destination(next_dest)
        self._schedule_arrival(camion_idx, t)

    def _process_depart(self, camion_idx: int, t: float) -> None:
        camion = self._camions[camion_idx]
        camion.state = True

        camion.set_destination(self._usine)
        camion.arrive()

        can_leave = camion.arrive_usine(self._usine, target_full=float(self._target_full_at_plant))
        if not can_leave:
            missing = int(max(0.0, float(self._target_full_at_plant) - float(camion.full)))
            prod_per_hour = float(self._usine.production_rate) / 24.0
            if prod_per_hour <= 0:
                camion.state = False
                return
            wait_h = missing / prod_per_hour
            camion.state = False
            self._schedule_depart(camion_idx, t + wait_h)
            return

        next_dest = self._choose_next_destination(camion, exclude=self._usine)
        camion.set_destination(next_dest)
        self._schedule_arrival(camion_idx, t)


    def simulate(self, duration_hours: float) -> None:
        duration_hours = float(duration_hours)

        self._current_time = 0.0
        self._revenue = 0.0
        self._travel_cost = 0.0
        self._production = 0.0

        while self._events and self._current_time < duration_hours:
            event_time, camion_idx, event_type = self._events.pop(0)

            if event_time > duration_hours:
                break

            dt = event_time - self._current_time
            self._production_usine(dt)
            self._consommation_clients(dt)
            self._current_time = event_time

            if event_type == "ARRIVAL":
                self._process_arrival(camion_idx, event_time)
            else:
                self._process_depart(camion_idx, event_time)
            
        
        return self.profit