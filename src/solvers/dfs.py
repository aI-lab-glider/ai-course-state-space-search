from collections import deque
from src.tree import Node, Tree
from src.base import Problem

class DFS():
    def __init__(self):
        self.start = Problem.initial
        self.frontier = deque()
        self.visited = {self.start}
        self.node = Node(self.start)
        self.tree = Tree(self.node)
    
    def run(self):
        self.frontier.append(self.node.state)
        while self.frontier:
            parent = self.frontier.popleft()
            if Problem.is_goal(self.node.state):
                return self.node
            children = deque()
            for child_node in self.tree.expand(Problem, parent):
                if child_node.state not in self.visited:
                    children.append(child_node.state)
                    self.visited.add(child_node.state)
            children.extend(self.frontier)
            self.frontier = children
        return None