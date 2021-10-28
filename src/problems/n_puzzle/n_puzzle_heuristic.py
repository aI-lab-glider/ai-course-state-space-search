from base import Heuristic
from problems.n_puzzle import NPuzzleState
from problems.n_puzzle import NPuzzleProblem


class NPuzzleHeuristic(Heuristic):

    def __init__(self, problem: NPuzzleProblem):
        self.problem = problem


    def apply(self, state: NPuzzleState) -> int:
        distance = ((state.x + state.y)**2 + self.problem.goal.y + self.problem.goal.x)
        return distance