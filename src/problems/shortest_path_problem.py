
class ShorthestPathProblem:
    def __init__(self, initial_state, goal_state):
        self.states = {}
        self.initial_state = initial_state
        self.goal_state = goal_state

    def actions(self, state):
        pass

    def transition_model(self, state, action):
        pass

    def action_cost(self, state, action, next_state):
        pass
