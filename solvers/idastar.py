from typing import Tuple, Optional
from base.solver import H, P, HeuristicSolver
from solvers.utils import LIFO, PriorityQueue
from tree import Node, Tree


class IDAStar(HeuristicSolver):
    def __init__(self, problem: P, heuristic: H):
        super().__init__(problem, heuristic)
        self.start = problem.initial
        self.root = Node(self.start, cost=0)
        self.tree = Tree(self.root)

    
    def solve(self) -> Optional[Node]:
        self.bound = self._fcost(self.root)
        while True:
            self.visited = dict()
            node, cost = self._cost_limited_search(self.root)
            if node is not None:
                return node
            self.bound = cost
            # print(self.bound)
            

    def _fcost(self, n: Node) -> float:
            return n.cost + self.heuristic(n.state)


    def _cost_limited_search(self, node: Node, limit: int) -> Tuple[Optional[Node], float]:
        if self.problem.is_goal(node.state):
            return node   

        cost = self._fcost(node)
        if cost > limit:
            return None, cost

        new_limit = float('inf')
        for child_node in self.tree.expand(self.problem, node):
            if child_node.has_cycle():
                continue
            candidate, candidate_cost = self._depth_limited_search(child_node, limit - 1)
            if candidate is not None:
                return candidate
            new_limit = min(new_limit, candidate_cost) 
        return None, new_limit
                
    def search_tree(self) -> Tree:
        return self.tree
