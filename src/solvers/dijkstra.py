from typing import Optional
from base.solver import Solver
from solvers.generic.best_first import BestFirstSearch
from tree.node import Node


class Dijkstra(Solver):
    def __init__(self, problem):
        super().__init__(problem)
        self.search = BestFirstSearch(problem, eval_fun=lambda node: node.cost)
    
    def solve(self) -> Optional[Node]:
        return self.search.solve()
        
        