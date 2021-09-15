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
    def aplly_action(self, state, action):
        """Returns new state resulting from taking given action"""
        raise NotImplementedError
