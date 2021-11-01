from abc import ABC, abstractmethod
from base.state import State
from typing import Union, List, TypeVar, Generic


S = TypeVar('S', bound=State)
A = TypeVar('A')

class Problem(ABC, Generic[S,A]):
    def __init__(self, initial: S):
        self.initial = initial

    @abstractmethod
    def actions(self, state: S) -> List[A]:
        """Generates actions to take from the given state"""
        raise NotImplementedError

    @abstractmethod
    def take_action(self, state: S, action: A) -> S:
        """Returns new state resulting from taking given action"""
        raise NotImplementedError

    @abstractmethod
    def action_cost(self, state: S, action: A, next_state: S) -> float:
        """Returns cost of an action"""
        raise NotImplementedError

    @abstractmethod
    def is_goal(self, state: S) -> bool:
        """Returns is given state is a goal state"""
        raise NotImplementedError
