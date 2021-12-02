from problems.pancake.pancake_problem import PancakeProblem
from base import Heuristic
from problems.pancake.pancake_state import PancakeState


class PancakeLargestPancakeHeuristic(Heuristic):
    def __init__(self, problem: PancakeProblem):
        self.problem = problem

    def __call__(self, state: PancakeState) -> float:
        if self.problem.is_goal(state):
            return 0
        return max(pancake for pancake, goal_pancake in zip(state.pancakes, self.problem.goal.pancakes)
                   if pancake != goal_pancake)
