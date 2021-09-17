from abc import ABC, abstractmethod


class Solver(ABC):
    def __init__(self, problem):
        self.problem = problem

    @abstractmethod
    def run():
        raise NotImplementedError