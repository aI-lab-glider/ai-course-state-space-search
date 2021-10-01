from base import Problem
from problems.rush_hour.vehicle import Vehicle
from problems.rush_hour.board import RushHourBoard
import numpy as np


class RushHourProblem(Problem):
    def __init__(self, initial: RushHourBoard, goal = Vehicle('X', 4, 2, 'H')):
        super().__init__(goal)
        self.initial = initial.get_board()


    def actions(self):
        pass


    def transition_model(self):
        pass


    def action_cost(self):
        return 1


    def is_goal(self):
        return self.goal in self.vehicles