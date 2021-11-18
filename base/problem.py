from __future__ import annotations
from abc import ABC, abstractmethod
from base.state import State
from typing import List, Optional, Tuple, TypeVar, Generic
from PIL.Image import Image

"""
Type variabiles used to define the generic types.
- S: any State class
"""
S = TypeVar('S', bound=State)
A = TypeVar('A')


class Problem(ABC, Generic[S, A]):
    """
    An interface for all the problems solvable by the classic graph search algorithms.

    Attributes:
    ===========
    initial: S
        an initial state — a starting point for the solvers
        set up in the __init__

    Abstract Methods:
    =================
        actions(state: S) -> List[A]:
            returns list of all the actions available at the given state
        take_action(state: S, action: A) -> S:
            applies the action the given state and returns the result (a new state)
        action_cost(state: S, action: A) -> float:
            returns cost of performing the given action at the given state
        is_goal(state: S) -> bool:
            checks if the given state is the goal of the problem

    Abstract Static Methods:
    ========================
        deserialize(text: Str) -> Self:
            creates a problem instance from the given textual representation
        to_image(state: S, size: Tuple[Int, Int]) -> Image:
            creates an image of the given size presenting the given state

    """

    def __init__(self, initial: S):
        self.initial = initial

    @abstractmethod
    def actions(self, state: S) -> List[A]:
        """ returns list of all the actions available at the given state """

    @abstractmethod
    def take_action(self, state: S, action: A) -> S:
        """ applies the action the given state and returns the result (a new state) """

    @abstractmethod
    def action_cost(self, state: S, action: A) -> float:
        """ returns cost of performing the given action at the given state """

    @abstractmethod
    def is_goal(self, state: S) -> bool:
        """ checks if the given state is the goal of the problem """

    @staticmethod
    @abstractmethod
    def deserialize(text: str) -> Problem[S, A]:
        """ creates a problem instance from the given textual representation """

    def to_image(self, state: S, size: Tuple[int, int]) -> Image:
        """ creates an image of the given size presenting the given state """


class ReversibleProblem(Problem[S,A], ABC, Generic[S,A]):
    """
    Interface for all the problems that can be reversed (goal and initial states are interchangeable).

    Attributes:
    ===========
        initial: S
            inherited from the :class:`Problem`
            set up in the __init__
        goal: S
            a goal state, the one we are looking for
            set up in the __init__

    Abstract Methods:
        reversed() -> Self:
            returns problem with swapped initial and goal states 
    """
    def __init__(self, initial: S, goal: S):
        super().__init__(initial)
        self.goal = goal


    @abstractmethod
    def reversed(self) -> ReversibleProblem[S, A]:
        """ returns problem with swapped initial and goal states """