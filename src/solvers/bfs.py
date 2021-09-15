from queue import Queue as FifoQueue
from src.tree import Node, Tree
from src.base import Problem

class BFS():
    def __init__(self):
        self.start = Problem.initial
        self.frontier = FifoQueue()
        self.visited = {self.start}
        self.node = Node(self.start)
        self.tree = Tree(self.node)
    
    def run(self):
        if Problem.is_goal(self.node.state):
            return self.node
        self.frontier.put(self.node.state)
        while self.frontier:
            parent = self.frontier.get()
            for child_node in self.tree.expand(Problem, parent):
                if Problem.is_goal(child_node.state):
                    return child_node
                if child_node.state not in self.visited:
                    self.frontier.put(child_node.state)
                    self.visited.add(child_node.state)
        return None


