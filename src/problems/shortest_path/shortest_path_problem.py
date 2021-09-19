from base import Problem


class ShorthestPathProblem(Problem):
    def __init__(self):
        super().__init__('Problem')

    def actions(self, state):
        pass

    def transition_model(self, state, action):
        pass

    def action_cost(self, state, action, next_state):
        pass
