from typing import Tuple, Optional
from base.solver import H, P, HeuristicSolver
from solvers.utils import PriorityQueue
from tree import Node, Tree


class IDAStar(HeuristicSolver):
    def __init__(self, problem: P, heuristic: H):
        super().__init__(problem, heuristic)
        self.start = problem.initial
        self.root = Node(self.start, cost=0)
        self.tree = Tree(self.root)

    
    def solve(self) -> Optional[Node]:
        if self.problem.is_goal(self.root.state):
            return self.root

        bound = self.heuristic(self.start)
        while True:
            node, cost = self._cost_limited_search(self.root, bound)
            if node is not None:
                return node
            if cost == bound:
                return None
            bound = cost

    
    def _cost_limited_search(self, root: Node, bound: float) -> Tuple[Optional[Node], float]:
        def fcost(n: Node) -> float:
            return n.cost + self.heuristic(n.state)
        
        frontier: LIFO = LIFO()
        visited = {self.start}
        frontier.push(root)
        new_bound = float('inf') 

        while not frontier.is_empty():
            node = frontier.pop()
            sorted_children = sorted(self.tree.expand(self.problem, node), key = fcost)
            for child_node in sorted_children:
                if child_node in visited:
                    continue
                if self.problem.is_goal(child_node.state):
                    return child_node, child_node.cost

                cost = fcost(child_node)
                if cost <= bound:
                    frontier.push(child_node)
                else:
                    new_bound = min(new_bound, cost)
            
        return None, new_bound
                
    def search_tree(self) -> Tree:
        return self.tree
