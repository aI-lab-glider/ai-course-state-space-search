import numpy as np


class RushHourBoard:
    def __init__(self, vehicles):
        self.vehicles = vehicles


    def get_board(self):
        board = np.array([[' '] * 6 for _ in range(6)])
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
        return self.vehicles == other.vehicles




    