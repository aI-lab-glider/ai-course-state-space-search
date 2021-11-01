from solvers.utils import Heap
from tree import Node, Tree


class BestFirstSearch:
    def __init__(self, problem, state, eval_fun=lambda node: node.cost):
        """With default eval_fun parameter, class implements uniform-cost search (Dijkstra) algorithm"""
        self.problem = problem
        self.start = state
        self.root = Node(self.start)
        self.frontier = Heap(key=eval_fun)
        self.visited = {self.start: self.root}
        self.tree = Tree(self.root)
    

    def run(self):
        self.frontier.push(self.root)
        while not self.frontier.is_empty():
            parent = self.frontier.pop()
            if self.problem.is_goal(parent.state):
                return parent
            for child_node in self.tree.expand(self.problem, parent):
                state = child_node.state
                if state not in self.visited or child_node.cost < self.visited[state].cost:
                    self.visited[state] = child_node
                    self.frontier.push(child_node)
        return None
