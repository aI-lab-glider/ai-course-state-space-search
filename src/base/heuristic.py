from abc import ABC, abstractmethod
from base import State


class Heuristic(ABC):

    @abstractmethod
    def apply(self, state: State):
        pass