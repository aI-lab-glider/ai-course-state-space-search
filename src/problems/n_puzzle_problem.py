from base import Problem
from state import NPuzzleState

class NPuzzleProblem(Problem):
    def __init__(self, initial, goal = None):
        super().__init__(initial,goal)

    def actions(self, state:NPuzzleState):

        actions_tab = []
        if self.valid(state.x,state.y+1,state.nx,state.ny):
            actions_tab.append("right")
        if self.valid(state.x,state.y-1,state.nx,state.ny):
            actions_tab.append("left")
        if self.valid(state.x-1,state.y,state.nx,state.ny):
            actions_tab.append("up")
        if self.valid(state.x+1,state.y,state.nx,state.ny):
            actions_tab.append("down")        
        
        return actions_tab

    def transition_model(self, state:NPuzzleState, action):
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
            state.matrix[state.x][state.y], state.matrix[state.x+move[0]][state.y+move[1]] = state.matrix[state.x+move[0]][state.y+move[1]], state.matrix[state.x][state.y]
            state.x = state.x + move[0]
            state.y = state.y + move[1]
            return state 

        print("transition model error")
        return None

    def action_cost(self, state:NPuzzleState, action, next_state:NPuzzleState):
        return 1

    def is_goal(self, state:NPuzzleState):
        if (state.matrix == self.goal.matrix):
            return True
        return False

    # artefakt, ale mi sie juz zmieniac nie chcialo
    def valid(self, x, y, nx, ny):
        if 0 <= x < nx and 0 <= y < ny:
            return True
        return False