from base.heuristic import Heuristic
from base.problem import Problem
from base.solver import HeuristicSolver
from base.state import State
from solvers.generic.bidirectional_search import BidirectionalSearch

from tree.tree import Tree


class NewBidrectionalAStar(HeuristicSolver):
    def __init__(self, problem: Problem, heuristic: Heuristic[State]):
        super().__init__(problem, heuristic)
        self.search = BidirectionalSearch(problem,
                                          lambda x: x.cost +
                                          heuristic(x.state),
                                          heuristic)

    def solve(self):
        return self.search.solve()

    def search_tree(self) -> Tree:
        return self.search.search_tree
