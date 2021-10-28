from abc import ABC, abstractmethod
from base import State


class Heuristic(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, state: State):
        raise NotImplementedError