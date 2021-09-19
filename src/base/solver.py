from abc import ABC, abstractmethod
from base.problem import Problem


class Solver(ABC):
    def __init__(self, problem: Problem):
        self.problem = problem

    @abstractmethod
    def run():
        raise NotImplementedError