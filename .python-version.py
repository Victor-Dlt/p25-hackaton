import pandas as pd
import numpy as np

class Client:
    def __init__(self, coord_x:float, coord_y:float, capacity: int, init:int, consumption:float):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.capacity = capacity
        self.init = init
        self.consumption = consumption

df= pd.read_csv("sujet-9-clients.csv")
type(df)
df=df.to_numpy()

C = []
for ligne in df :
    client = Client(ligne[0], ligne[1],ligne[2],ligne[3],ligne[4])
    C.append(client)
print (C[0])