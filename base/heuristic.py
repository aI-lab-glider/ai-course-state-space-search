from abc import ABC, abstractmethod
from base import State, Problem

from typing import TypeVar, Generic, Any, cast

S = TypeVar('S', bound=State)


class Heuristic(ABC, Generic[S]):
    """
    Class that calculates expected reward for state
    """

    @abstractmethod
    def __init__(self, problem: Problem[S, Any]) -> None:
        pass

    @abstractmethod
    def __call__(self, state: S) -> float:
        pass


class NoHeuristic(Heuristic[S]):
    def __init__(self):
        super().__init__(cast(Problem, None))

    def __call__(self, problem: Problem[S, Any]) -> float:
        return 0
