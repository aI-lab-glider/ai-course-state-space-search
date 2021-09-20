from base import Problem
from problems.sudoku.sudoku_state import SudokuState
from typing import Union


class SudokuProblem(Problem):
    def __init__(self, initial: SudokuState, goal: SudokuState = None):
        super().__init__(initial, goal)


    def actions(self, state: SudokuState):
        pass


    def transition_model(self, state: SudokuState, action: Union[str, int]) -> SudokuState:
        pass


    def action_cost(self, state: SudokuState, action: Union[str, int], next_state: SudokuState) -> int:
        return 1


    def is_goal(self, state: SudokuState) -> bool:
        pass

    def possible_move(self, x: int, y: int, n: int) -> bool:
        pass
