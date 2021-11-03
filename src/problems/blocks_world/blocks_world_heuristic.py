


from typing import Dict, List
from base.heuristic import Heuristic
from problems.blocks_world.blocks_world_problem import BlocksWorldProblem, BlocksWorldState

class BlocksWorldNaiveHeuristic(Heuristic):

    def __init__(self, problem: BlocksWorldProblem) -> None:
        super().__init__(problem)
        self.expected_columns = self._calculate_expected_columns(problem.goal)
        self.expected_fundaments = self._calculate_expected_fundaments(problem.goal)

    def _calculate_expected_columns(self, goal: BlocksWorldState) -> Dict[str, int]:
        expected_columns = dict()
        for i,col in enumerate(goal.columns):
            for b in col:
                expected_columns[b] = i
        return expected_columns

    def _calculate_expected_fundaments(self, goal: BlocksWorldState) -> Dict[str, List[str]]:
        expected_fundaments = dict()
        for col in goal.columns:
            for i,b in enumerate(col):
                expected_fundaments[b] = col[:i]
        return expected_fundaments

    def __call__(self, state: BlocksWorldState) -> int:
        wrong_cols = 0
        wrong_fundaments = 0
        for ic, col in enumerate(state.columns):
            for ib, b in enumerate(col):
                if self.expected_columns[b] != ic:
                    wrong_cols += 1
                elif self.expected_fundaments[b] != col[:ib]:
                    wrong_fundaments += 1
        return wrong_cols + 2 * wrong_fundaments