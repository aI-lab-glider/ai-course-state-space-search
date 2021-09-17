# from queue import PriorityQueu
from src.solvers.utils import Heap
from src.tree import Node, Tree


class BestFirstSearch:
    def __init__(self, problem, state):
        self.problem = problem
        self.start = state
        self.frontier = Heap(maxheap=False, key=lambda x: x.cost)
        self.visited = {self.start: self.root}
        self.root = Node(self.start)
        self.tree = Tree(self.root)
    

    def run(self):
        self.frontier.put(self.root)
        while not self.frontier.empty():
            parent = self.frontier.pop()
            if self.problem.is_goal(parent.state):
                return parent
            for child_node in self.tree.expand(self.problem, parent):
                state = child_node.state
                if state not in self.visited or child_node.cost < self.visited[state].cost:
                    self.visited[state] = child_node
                    self.frontier.add(child_node)
        return None
