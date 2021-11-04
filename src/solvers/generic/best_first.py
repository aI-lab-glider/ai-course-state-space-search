from typing import Callable, Optional
from base.problem import Problem
from solvers.utils import PriorityQueue, Queue
from tree import Node, Tree


class BestFirstSearch():
    def __init__(self, problem: Problem, eval_fun: Callable[[Node], float]):
        self.problem = problem
        self.eval_fun = eval_fun
        self.start = problem.initial
        self.root = Node(self.start)
        self.frontier:PriorityQueue = PriorityQueue(eval_fun)
        self.visited = {self.start: self.root.cost}
        self.tree = Tree(self.root)
    

    def solve(self) -> Optional[Node]:
        if self.problem.is_goal(self.root.state):
            return self.root

        self.frontier.push(self.root)
        while not self.frontier.is_empty():
            parent = self.frontier.pop()
            if self.problem.is_goal(parent.state):
                return parent
            for child_node in self.tree.expand(self.problem, parent):
                state = child_node.state
                if state not in self.visited or child_node.cost < self.visited[state]:
                    self.visited[state] = child_node.cost
                    self.frontier.push(child_node)
        return None
