from typing import Callable, Tuple, Optional
from base.state import State
from solvers.utils import Heap
from tree import Node, Tree


class IDAStar:
    def __init__(self, problem, state, heuristic: Callable[[State], float]):
        self.problem = problem
        self.start = state
        self.root = Node(self.start, cost=0)
        self.tree = Tree(self.root)
        self.heuristic = heuristic

    
    def run(self, max_cost: float=float('inf')) -> Optional[Node]:
        if self.problem.is_goal(self.root.state):
            return self.root

        bound = self.heuristic(self.start)
        while bound < max_cost:
            is_goal, node, cost = self._cost_limited_search(self.root, bound)
            if is_goal:
                return node 
            bound = cost
        return None

    
    def _cost_limited_search(self, root: Node, bound: float) -> Tuple[bool, Optional[Node], float]:
        frontier:Heap = Heap(lambda x: x.cost + self.heuristic(x.state))
        frontier.push(root)
        new_bound = np.inf # next iteration bound
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
                
