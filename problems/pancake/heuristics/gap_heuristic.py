from problems.pancake.pancake_problem import PancakeProblem
from base import Heuristic
from problems.pancake.pancake_state import PancakeState


class PancakeGapHeuristic(Heuristic):
    def __init__(self, problem: PancakeProblem):
        self.problem = problem

    def __call__(self, state: PancakeState) -> float:
        return sum([1 for i in range(self.problem.n_pancakes) if abs(state.pancakes[i + 1] - state.pancakes[i]) != 1])
