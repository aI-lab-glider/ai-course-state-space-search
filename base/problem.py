from __future__ import annotations
from abc import ABC, abstractmethod
from base.state import State
from typing import List, Optional, Tuple, TypeVar, Generic
from PIL.Image import Image

S = TypeVar('S', bound=State)
A = TypeVar('A')


class Problem(ABC, Generic[S, A]):
    """
    Class that contains all static information about problem that we
    trying to solve.

    Args: 
        initial (:class:`State`) - state from which we want to start solving.
    """

    def __init__(self, initial: S, goal: S):
        self.initial = initial
        self.goal = goal

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

    def is_goal(self, state: S) -> bool:
        """Checks if given state is a goal state"""
        return state == self.goal

    @staticmethod
    @abstractmethod
    def deserialize(text: str) -> Problem[S, A]:
        """Helper function, that allows to create :class:`Problem` from its text representation."""

    def to_image(self, state: S, size: Tuple[int, int]) -> Optional[Image]:
        """Converts state to its image representation."""
