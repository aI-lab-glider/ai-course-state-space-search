from typing import Optional
from base.solver import P, HeuristicSolver
from solvers.utils import PriorityQueue, Queue
from tree import Node, Tree


class UninformedSearch():
    def __init__(self, problem: P, queue: Queue):
        self.problem = problem
        self.start = problem.initial
        self.frontier = queue
        self.visited = {self.start}
        self.root = Node(self.start)
        self.tree = Tree(self.root)


    def solve(self):
        if self.problem.is_goal(self.root.state):
            return self.root

        self.frontier.push(self.root)
        while not self.frontier.is_empty():
            parent = self.frontier.pop()
            for child_node in self.tree.expand(self.problem, parent):
                if self.problem.is_goal(child_node.state):
                    return child_node
                if child_node.state not in self.visited:
                    self.frontier.push(child_node)
                    self.visited.add(child_node.state)
        return None
