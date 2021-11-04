from typing import Tuple, Optional
from base.solver import P, Solver
from solvers.utils import PriorityQueue
from solvers.utils import LIFO
from tree import Node, Tree


class IDDFS(Solver):
    def __init__(self, problem: P):
        self.problem = problem
        self.start = problem.initial
        self.root = Node(self.start)
        self.tree = Tree(self.root)


    def solve(self) -> Optional[Node]:
        if self.problem.is_goal(self.root.state):
            return self.root
        depth = 1
        while True:
            is_goal, node, nodes_left = self._depth_limited_search(self.root, depth)
            if is_goal:
                return node 
            if not nodes_left:
                return None
            depth += 1  
    

    def _depth_limited_search(self, root: Node, max_depth: int) -> Tuple[bool, Optional[Node], bool]:
        frontier:LIFO = LIFO()
        visited = {self.start}
        frontier.push(root)
        depth = 0
        nodes_left = False
        while not frontier.is_empty():
            node = frontier.pop()
            for child_node in self.tree.expand(self.problem, node):
                if child_node.state in visited:
                    continue
                if self.problem.is_goal(child_node.state):
                    return True, child_node, nodes_left
                if depth < max_depth:
                    frontier.push(child_node)
                    visited.add(child_node.state)
                else:
                    nodes_left = True
        return False, None, nodes_left


    def search_tree(self) -> Tree:
        return self.tree
        