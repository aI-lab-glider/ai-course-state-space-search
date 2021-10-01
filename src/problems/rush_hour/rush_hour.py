from base import Problem
from problems.rush_hour.vehicle import Vehicle
from typing import Sequence
import numpy as np


class RushHourProblem():
    def __init__(self, vehicles: Sequence[Vehicle], goal = Vehicle('X', 4, 2, 'H')):
        self.goal = goal
        self.vehicles = vehicles


    def __hash__(self):
        return hash(self.__str__())


    def __str__(self):
        s = '\n'
        for line in self.get_board():
            s += ''.join(line) + '\n'
        return s


    def get_board(self):
        board = np.array([[' '] * 6 for _ in range(6)])
        for vehicle in self.vehicles:
            x, y = vehicle.x, vehicle.y
            xEnd, yEnd = vehicle.xEnd, vehicle.yEnd
            board[y:yEnd+1, x:xEnd+1] = vehicle.id
        return board


    def actions(self):
        pass


    def transition_model(self):
        pass


    def action_cost(self):
        return 1


    def is_goal(self):
        return self.goal in self.vehicles