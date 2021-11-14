import numpy as np
from typing import Set, Tuple
from problems.rush_hour.vehicle import RushHourVehicle
from base import State


class RushHourBoard(State):
    def __init__(self, vehicles: Set[RushHourVehicle], shape: Tuple[int, int] = (6, 6)):
        self.vehicles = vehicles
        self.shape = shape

    def get_board(self):
        board = np.full(self.shape, ' ')
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            xEnd, yEnd = vehicle.xEnd, vehicle.yEnd
            board[y:yEnd+1, x:xEnd+1] = vehicle.id
        return board

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self) -> str:
        s = '\n'
        for line in self.get_board():
            s += ''.join(line) + '\n'
        return s

    def __eq__(self, other):
        return (self.get_board() == other.get_board()).all()
