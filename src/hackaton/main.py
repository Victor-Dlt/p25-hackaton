import pandas as pd
import numpy as np
from .Client import Client


def main() -> None:
    df= pd.read_csv("sujet-9-clients.csv")
    df=df.to_numpy()

    C = []
    for ligne in df :
        client = Client(ligne[0], ligne[1],ligne[2],ligne[3],ligne[4])
        C.append(client)