from src.base.problem import Problem


class NPuzzleProblem(Problem):
    def __init__(self, initial, goal):
        super().__init__(initial, goal)

    def actions(self, state):
        nx = len(state)
        ny = len(state[0])
        x = 0
        y = 0
        for i in range(nx):
            for j in range(ny):
                if state[i][j] == 0:
                    x = i
                    y = j
        actions_tab = []
        if 0 <= x < nx and 0 <= y + 1 < ny:
            actions_tab.append("up")
        if 0 <= x < nx and 0 <= y - 1 < ny:
            actions_tab.append("down")
        if 0 <= x + 1 < nx and 0 <= y < ny:
            actions_tab.append("right")
        if 0 <= x - 1 < nx and 0 <= y < ny:
            actions_tab.append("left")

        return actions_tab


    def transition_model(self, state, action):
        nx = len(state)
        ny = len(state[0])
        x = 0
        y = 0
        for i in range(nx):
            for j in range(ny):
                if state[i][j] == 0:
                    x = i
                    y = j

        if action == "up":
            matrix = state
            matrix[x][y], matrix[x][y + 1] = matrix[x][y + 1], matrix[x][y]
            return matrix
        if action == "down":
            matrix = state
            matrix[x][y], matrix[x][y - 1] = matrix[x][y - 1], matrix[x][y]
            return matrix
        if action == "right":
            matrix = state
            matrix[x][y], matrix[x + 1][y] = matrix[x + 1][y], matrix[x][y]
            return matrix
        if action == "left":
            matrix = state
            matrix[x][y], matrix[x - 1][y] = matrix[x - 1][y], matrix[x][y]
            return matrix

    def action_cost(self, state, action, next_state):
        return 1
