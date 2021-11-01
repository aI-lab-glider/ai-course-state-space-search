from base import Problem
from problems.n_puzzle import NPuzzleState
from typing import Union, List
from copy import deepcopy

from problems.n_puzzle.n_puzzle_action import NPuzzleAction


class NPuzzleProblem(Problem[NPuzzleState, NPuzzleAction]):
    def __init__(self, initial: NPuzzleState, goal: NPuzzleState):
        super().__init__(initial)
        self.goal = goal

    def actions(self, state: NPuzzleState) -> List[NPuzzleAction]:
        return [shift for shift in NPuzzleAction 
                if self.valid(state.x + shift.value[0], 
                              state.y + shift.value[1],
                              state.nx, state.ny)]

    def take_action(self, state: NPuzzleState, action: NPuzzleAction) -> NPuzzleState:
        shift_x, shift_y = action.value
        if self.valid(state.x+shift_x, state.y+shift_y, state.nx, state.ny):
            state2 = deepcopy(state)
            state2.matrix[state2.x][state2.y] = state2.matrix[state2.x+shift_x][state2.y+shift_y]
            state2.matrix[state2.x+shift_x][state2.y+shift_y] = state.matrix[state.x][state.y]
            state2.x = state2.x + shift_x
            state2.y = state2.y + shift_y
            return state2

        raise Exception("Illegal action")


    def action_cost(self, state:NPuzzleState, action: NPuzzleAction, next_state:NPuzzleState) -> float:
        return 1


    def is_goal(self, state: NPuzzleState) -> bool:
        return self.goal.matrix == state.matrix


    def valid(self, x: int, y: int, nx: int, ny: int) -> bool:
        return 0 <= x < nx and 0 <= y < ny