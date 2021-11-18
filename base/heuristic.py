from abc import ABC, abstractmethod
from base import State, Problem

from typing import TypeVar, Generic, Any, cast

S = TypeVar('S', bound=State)


class Heuristic(ABC, Generic[S]):
    """
    Interface representing heuristics, functions that approximiate distance
    from the given state to the problem goal.

    Abstract Methods:
    =================
    __init__(problem: Problem[S, Any]):
        creates a heuristic for the given problem
        this method should use to precalculate helper functions
    __call__(state: S) -> float:
        calculates approximiate distance from the given state to the goal
    """

    @abstractmethod
    def __init__(self, problem: Problem[S, Any]) -> None:
        """ creates a heuristic for the given problem
            this method should use to precalculate helper functions
        """

    @abstractmethod
    def __call__(self, state: S) -> float:
        """ calculates approximiate distance from the given state to the goal """


class NoHeuristic(Heuristic[S]):
    """
    The most basic heuristic.
    Doesn't provide any info, always returns 0.
    """
    def __init__(self):
        super().__init__(cast(Problem, None))

    def __call__(self, state: S) -> float:
        return 0
