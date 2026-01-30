import pandas as pd
import numpy as np

class Client:
    def __init__(self, coord_x:float, coord_y:float, capacity: int, init:int, consumption:float):
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.capacity = capacity
        self.init = init
        self.consumption = consumption

