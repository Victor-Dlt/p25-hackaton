import pandas as pd
import numpy as np

class Client:
    def __init__(self, coord_x:float, coord_y:float, capacity: int, init:int, consumption:float):
        self.x = coord_x
        self.y = coord_y
        self.capacity = capacity
        self.empty = init
        self.full = capacity - init
        self.consumption = consumption

