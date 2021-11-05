from typing import Optional, Set
from base.solver import P, Solver
from base.state import State
from tree import Node, Tree


class DFSRecursive(Solver):
    def __init__(self, problem: P):
        super().__init__(problem)
        self.start = problem.initial
        self.visited: Set[State] = set()
        self.root = Node(self.start)
        self.tree = Tree(self.root)


    def dfs(self, node: Node) -> Optional[Node]:
        if self.problem.is_goal(node.state):
            return node
        if node.state in self.visited:
            return None
        self.visited.add(node.state)
        for child in self.tree.expand(self.problem, node):
            candidate = self.dfs(child)
            if candidate is not None:
                return candidate 
        return None   

    def solve(self) -> Optional[Node]:
        return self.dfs(self.root)

    def search_tree(self) -> Tree:
        return self.tree
