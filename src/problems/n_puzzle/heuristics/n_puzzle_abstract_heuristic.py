from abc import ABC
from typing import Dict, Tuple
from base import Heuristic
from problems.n_puzzle import NPuzzleState
from problems.n_puzzle import NPuzzleProblem


class NPuzzleAbstractHeuristic(Heuristic[NPuzzleState], ABC):

    def __init__(self, problem: NPuzzleProblem):
        self.problem = problem
        self.goal_coords = self.positions(problem.goal)

    def positions(self, goal: NPuzzleState) -> Dict[int,Tuple[int,int]]:
        positions: Dict[int,Tuple[int,int]] = dict()
        for y,row in enumerate(goal.matrix):
            for x,cell in enumerate(row):
                if cell != 0:
                    positions[cell] = (x,y)
        return positions
