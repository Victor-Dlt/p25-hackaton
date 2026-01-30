import pandas as pd
import numpy as np
from .Camion import Camion
from .Client import Client
from .SimulationHandler import SimulationHandler
from .Usine import Usine


def main() -> None:
    df= pd.read_csv("sujet-9-clients.csv")
    df=df.to_numpy()

    clients = []
    for ligne in df :
        client = Client(ligne[0], ligne[1],ligne[2],ligne[3],ligne[4])
        clients.append(client)

    usine = Usine(217.876, 6753.44, 510.83, 0, 437)
    camions = []

    for i in range(30):
        camion = Camion(
            capacity = 80,
            x = (clients[i].x + usine.x)/2,
            y = (clients[i].y + usine.y)/2,
            to_x = 0,
            to_y = 0,
            full = 20,
            empty = 10
        )
        camions.append(camion)

    sim = SimulationHandler(camions=camions, usine=usine, clients=clients, speed_kmh=70, target_full_at_plant=50)

    revenue = sim.simulate(24*30)  # Simuler pendant 30 jours

    print(revenue)