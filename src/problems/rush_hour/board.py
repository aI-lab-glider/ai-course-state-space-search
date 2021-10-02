from problems.rush_hour.vehicle import RushHourVehicle
from typing import Sequence
import numpy as np


class RushHourBoard():
    def __init__(self, vehicles: Sequence[RushHourVehicle]):
        self.vehicles = vehicles


    def __str__(self):
        s = '\n'
        for line in self.get_board():
            s += ''.join(line) + '\n'
        return s

    # method or variable ???
    def get_board(self):
        board = np.array([[' '] * 6 for _ in range(6)])
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            xEnd, yEnd = vehicle.xEnd, vehicle.yEnd
            board[y:yEnd+1, x:xEnd+1] = vehicle.id
        return board

    