from collections import deque
from typing import Deque
from base.solver import P, Solver
from solvers.generic.uninformed import UninformedSearch
from solvers.utils import LIFO
from tree import Node, Tree


class DFSIter(Solver):
    def __init__(self, problem:P):
        super().__init__(problem)
        self.search = UninformedSearch(problem, LIFO())

    def solve(self):
        return self.search.solve()

    def search_tree(self) -> Tree:
        return self.search.tree