from queue import Queue as FifoQueue
from base.solver import P, Solver
from solvers.generic.uninformed import UninformedSearch
from solvers.utils import FIFO
from tree import Node, Tree


class BFS(Solver):
    def __init__(self, problem:P):
        super().__init__(problem)
        self.search = UninformedSearch(problem, FIFO())

    def solve(self):
        return self.search.solve()


