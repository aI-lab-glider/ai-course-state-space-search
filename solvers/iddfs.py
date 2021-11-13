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
        # TODO:
        # - if the root node is a goal, just return it
        #   tip. use 'is_goal' method from Problem
        # - set depth to 0
        # - run self._depth_limited search
        #   * if it returned a node, return it!
        #   * if there is no nodes left, return None
        #   * otherwise increment depth and repeat the limited search
        limit = 0
        while True:
            node = self._depth_limited_search(self.root, limit)
            if node is not None:
                return node
            limit += 1

    def _depth_limited_search(self, node: Node, limit: int) -> Optional[Node]:
        if self.problem.is_goal(node.state):
            return node

        if limit <= 0:
            return None

        for child_node in self.tree.expand(self.problem, node):
            if child_node.has_cycle():
                continue
            candidate = self._depth_limited_search(child_node, limit - 1)
            if candidate is not None:
                return candidate
        return None

    def search_tree(self) -> Tree:
        return self.tree
