from base import Heuristic
from problems.n_puzzle import NPuzzleState
from problems.n_puzzle import NPuzzleProblem

import numpy as np
from math import sqrt



class NPuzzleEuclideanHeuristic(Heuristic[NPuzzleState]):

    def __init__(self, problem: NPuzzleProblem):
        self.problem = problem


    def __call__(self, state: NPuzzleState) -> float:
        distance = np.sum(sqrt((state.x - self.problem.goal.x)**2 + (state.y - self.problem.goal.y)**2 ))
        return distance