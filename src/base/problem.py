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


    @abstractmethod
    def action_cost(self, state, action):
        """Return cost of the given action"""
        raise NotImplementedError


    # Probably we want to keep heuristic as separate function
    @abstractmethod
    def estimate_path_cost(self, state):
        """Heuristic that estimates path cost from the given state to the goal state"""
        raise NotImplementedError
    

