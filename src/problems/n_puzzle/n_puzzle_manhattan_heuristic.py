from base import Heuristic
from problems.n_puzzle import NPuzzleState
from problems.n_puzzle import NPuzzleProblem
import numpy as np


class NPuzzleManhattanHeuristic(Heuristic):

    def __init__(self, problem: NPuzzleProblem):
        self.problem = problem


    def apply(self, state: NPuzzleState) -> int:
        distance = np.sum(abs(state.x - self.problem.goal.x) + abs(state.y - self.problem.goal.y))
        return distance