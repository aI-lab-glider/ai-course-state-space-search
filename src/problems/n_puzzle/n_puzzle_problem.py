from base import Problem
from problems.n_puzzle.n_puzzle_state import NPuzzleState
from typing import Union, List
from copy import deepcopy


class NPuzzleProblem(Problem):
    def __init__(self, initial: NPuzzleState, goal: NPuzzleState = None):
        super().__init__(initial,goal)

    def actions(self, state: NPuzzleState) -> List[Union[str, int]]:
        actions_tab = []
        if self.valid(state.x+1, state.y, state.nx, state.ny):
            actions_tab.append("down")
        if self.valid(state.x-1, state.y, state.nx, state.ny):
            actions_tab.append("up")
        if self.valid(state.x, state.y+1, state.nx, state.ny):
            actions_tab.append("right")
        if self.valid(state.x, state.y-1, state.nx, state.ny):
            actions_tab.append("left")
        
        return actions_tab


    def transition_model(self, state: NPuzzleState, action: Union[str, int]) -> NPuzzleState:
        move = [0,0]
        if action == "right":
            move = [0,1]
        if action == "left":
            move = [0,-1]
        if action == "up":
            move = [-1,0]
        if action == "down":
            move = [1,0]


        if self.valid(state.x+move[0], state.y+move[1], state.nx, state.ny):
            state2 = deepcopy(state)
            state2.matrix[state2.x][state2.y], state2.matrix[state2.x+move[0]][state2.y+move[1]] = state2.matrix[state2.x+move[0]][state2.y+move[1]], state.matrix[state.x][state.y]
            state2.x = state2.x + move[0]
            state2.y = state2.y + move[1]
            return state2

        print("Transition model error")
        return None


    def action_cost(self, state:NPuzzleState, action: Union[str, int], next_state:NPuzzleState) -> int:
        return 1


    def is_goal(self, state: NPuzzleState) -> bool:
        return self.goal.matrix == state.matrix


    def valid(self, x: int, y: int, nx: int, ny: int) -> bool:
        return 0 <= x < nx and 0 <= y < ny