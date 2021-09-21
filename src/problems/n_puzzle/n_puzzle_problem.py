from base import Problem
from problems.n_puzzle import NPuzzleState
from typing import Union, List
from copy import deepcopy


class NPuzzleProblem(Problem):
    def __init__(self, initial: NPuzzleState, goal: NPuzzleState = None):
        super().__init__(initial,goal)

    def actions(self, state: NPuzzleState) -> List[Union[str, int]]:
        actions_tab = []

        shifts =[
        (1, 0, "down"),
        (-1,0, "up"),
        (0,1, "right"),
        (0,-1, "left")
        ]

        actions_tab = [shift_name for shift_x, shift_y, shift_name in shifts if self.valid(state.x + shift_x, state.y + shift_y, state.nx, state.ny)]
        
        return actions_tab


    def transition_model(self, state: NPuzzleState, action: Union[str, int]) -> NPuzzleState:
        move = {
        "right": (0,1),
        "left": (0, -1),
        "up": (-1, 0),
        "down": (1, 0)
        }[action]

        if self.valid(state.x+move[0], state.y+move[1], state.nx, state.ny):
            state2 = deepcopy(state)
            state2.matrix[state2.x][state2.y], state2.matrix[state2.x+move[0]][state2.y+move[1]] = state2.matrix[state2.x+move[0]][state2.y+move[1]], state.matrix[state.x][state.y]
            state2.x = state2.x + move[0]
            state2.y = state2.y + move[1]
            return state2

        raise Exception("Transition model error")


    def action_cost(self, state:NPuzzleState, action: Union[str, int], next_state:NPuzzleState) -> int:
        return 1


    def is_goal(self, state: NPuzzleState) -> bool:
        return self.goal.matrix == state.matrix


    def valid(self, x: int, y: int, nx: int, ny: int) -> bool:
        return 0 <= x < nx and 0 <= y < ny