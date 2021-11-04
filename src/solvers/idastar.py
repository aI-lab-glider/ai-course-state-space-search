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
            is_goal, node, cost = self._cost_limited_search(self.root, bound)
            if is_goal:
                return node 
            if cost == bound:
                return None
            bound = cost

    
    def _cost_limited_search(self, root: Node, bound: float) -> Tuple[bool, Optional[Node], float]:
        frontier:PriorityQueue = PriorityQueue(lambda x: x.cost + self.heuristic(x.state))
        frontier.push(root)
        new_bound = float('inf') # next iteration bound
        while not frontier.is_empty():
            node = frontier.pop()
  
            for child_node in self.tree.expand(self.problem, node):
                if self.problem.is_goal(child_node.state):
                    return True, child_node, child_node.cost
                cost = child_node.cost + self.heuristic(child_node.state)
                if cost <= bound:
                    frontier.push(child_node)
                else:
                    new_bound = min(new_bound, cost)
        return False, None, new_bound
                
    def search_tree(self) -> Tree:
        return self.tree
