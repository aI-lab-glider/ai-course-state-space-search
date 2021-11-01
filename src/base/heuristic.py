from abc import ABC, abstractmethod
from base import State

from typing import TypeVar, Generic

S = TypeVar('S', bound=State)

class Heuristic(ABC, Generic[S]):

    @abstractmethod
    def __call__(self, state: S) -> float:
        pass