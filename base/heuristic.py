from abc import ABC, abstractmethod
from base import State, Problem

from typing import TypeVar, Generic, Any

S = TypeVar('S', bound=State)


class Heuristic(ABC, Generic[S]):
    """
    Class that calculates expected reward for
    """

    @abstractmethod
    def __init__(self, problem: Problem[S, Any]) -> None:
        pass

    @abstractmethod
    def __call__(self, state: S) -> float:
        pass
