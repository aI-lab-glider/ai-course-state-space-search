from abc import ABC, abstractmethod


class Problem(ABC):
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    @abstractmethod
    def actions(self, state):
        """Generates actions to take from the given state"""
        raise NotImplementedError

    @abstractmethod
    def transition_model(self, state, action):
        """Returns new state resulting from taking given action"""
        raise NotImplementedError

    @abstractmethod
    def action_cost(self, state, action, next_state):
        """Returns cost of an action"""
        raise NotImplementedError

    @abstractmethod
    def is_goal(self, state):
        """Returns is given state is a goal state"""
        raise NotImplementedError
