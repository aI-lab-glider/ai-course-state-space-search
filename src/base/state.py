from abc import ABC, abstractmethod


class State(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __hash__(self):
        raise NotImplementedError

    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    @abstractmethod
    def display(self):
        raise NotImplementedError
