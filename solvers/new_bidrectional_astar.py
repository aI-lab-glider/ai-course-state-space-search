from typing import Reversible
from base.heuristic import Heuristic
from base.problem import Problem, ReversibleProblem
from base.solver import BidirectionalHeuristicSolver, HeuristicSolver
from base.state import State
from solvers.generic.bidirectional_search import BidirectionalSearch

from tree.tree import Tree


class NBAstar(BidirectionalHeuristicSolver):
    def __init__(self, problem: ReversibleProblem, 
                       primary_heuristic: Heuristic[State], 
                       opposite_heuristic: Heuristic[State]):
        super().__init__(problem, primary_heuristic, opposite_heuristic)
        self.search = BidirectionalSearch(problem,
                                          primary_heuristic,
                                          opposite_heuristic)

    def solve(self):
        return self.search.solve()

    def search_tree(self) -> Tree:
        return self.search.search_tree
