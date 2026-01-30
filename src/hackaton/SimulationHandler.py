
from .Camion import Camion

class SimulationHandler:
    def __init__(self, camions : [Camion]) -> None:
        self._events = [] # liste des temps des futurs événements en secondes
        self._camions = camions

    @property
    def events(self) -> list[float]:
        return self._events
    
    def add_event(self, event_time: float) -> None:
        self._events.append(event_time)
        self._events.sort()

    def simulate(self, duration: float) -> None:
        current_time = 0.0
        while self._events and current_time < duration:
            next_event_time = self._events.pop(0)
            if next_event_time > duration:
                break
            current_time = current_time + next_event_time

            for camion in self._camions:
                if camion.state:
                    # il va vers le meilleur client / usine
                    
                    pass

                # stationnement 
            


    