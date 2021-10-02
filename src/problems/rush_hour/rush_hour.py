from base import Problem
from problems.rush_hour.vehicle import RushHourVehicle
from problems.rush_hour.board import RushHourBoard
import numpy as np


class RushHourProblem(Problem):
    def __init__(self, initial: RushHourBoard, goal = RushHourVehicle('X', 4, 2, 'H')):
        super().__init__(goal)
        self.initial = initial.get_board()


    def actions(self, board: RushHourBoard, vehicle: RushHourVehicle):
        actions = []

        shifts = {
            'V': [('up', -1, 0), ('down', 1, 0)],
            'H': [('left', 0, -1), ('right', 0, 1)]
        }

        for shift, y, x in shifts[vehicle.orientation]:
            if self.valid(vehicle.x+x, vehicle.y+y) and (shift == 'up' or 'left'):
                if board[vehicle.y+y, vehicle.x+x] == ' ':
                    actions.append(shift)
            if self.valid(vehicle.xEnd+x, vehicle.yEnd+y) and (shift == 'down' or 'right'):
                if board[vehicle.yEnd+y, vehicle.xEnd+x] == ' ':
                    actions.append(shift)                    

        return actions


    def transition_model(self):
        pass


    def action_cost(self):
        return 1


    def is_goal(self):
        return self.goal in self.vehicles


    def valid(self, x: int, y: int, nx = 6, ny = 6) -> bool:
        return 0 <= x < nx and 0 <= y < ny