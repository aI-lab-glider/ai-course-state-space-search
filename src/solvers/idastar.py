from typing import Callable, Tuple, Optional
from queue import LifoQueue
import numpy as np
from base.state import State
from tree import Node, Tree


class IDAStar:
    def __init__(self, problem, state):
        self.problem = problem
        self.start = state
        self.root = Node(self.start, cost=0)
        self.tree = Tree(self.root)

    
    def run(self, heuristic: Callable[[State], int], max_cost: int=np.inf) -> Optional[Node]:
        bound = heuristic(self.start)
        while bound < max_cost:
            is_goal, node, cost = self.cost_limited_search(self.root, heuristic, bound)
            if is_goal:
                return node 
            bound = cost
        return None

    
    def _cost_limited_search(self, root: Node, heuristic: Callable[[State], int], bound: int) -> Tuple[bool, Optional[Node], int]:
        if self.problem.is_goal(root.state):
            return True, root, root.cost
        frontier = LifoQueue()
        frontier.put(root)
        new_bound = np.inf # next iteration bound
        while frontier:
            node = frontier.get()
            for child_node in self.tree.expand(self.problem, node):
                if self.problem.is_goal(child_node.state):
                    return True, node, node.cost
                if child_node.cost + heuristic(child_node.state) <= bound:
                    frontier.put(child_node)
                else:
                    new_bound = min(new_bound, child_node.cost + heuristic(child_node.state))
        return False, None, new_bound
                
