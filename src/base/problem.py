from abc import ABC, abstractmethod
from base.state import State
from typing import Union, List

class Problem(ABC):
    def __init__(self, initial: State, goal: State = None):
        self.initial = initial
        self.goal = goal

    @abstractmethod
    def actions(self, state: State) -> List[Union[str, int]]:
        """Generates actions to take from the given state"""
        raise NotImplementedError

    @abstractmethod
    def transition_model(self, state: State, action: Union[str, int]) -> State:
        """Returns new state resulting from taking given action"""
        raise NotImplementedError

    @abstractmethod
    def action_cost(self, state: State, action: Union[str, int], next_state: State) -> int:
        """Returns cost of an action"""
        raise NotImplementedError

    @abstractmethod
    def is_goal(self, state: State) -> bool:
        """Returns is given state is a goal state"""
        raise NotImplementedError
