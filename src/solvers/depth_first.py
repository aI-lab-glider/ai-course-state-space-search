from collections import deque
from src.tree import Node, Tree

class DFS():
    def __init__(self, problem, state):
        self.problem = problem
        self.start = state
        self.frontier = deque()
        self.visited = {self.start}
        self.root = Node(self.start)
        self.tree = Tree(self.root)
    
    def run(self):
        self.frontier.append(self.root)
        while self.frontier:
            parent = self.frontier.popleft()
            if self.problem.is_goal(parent.state):
                return self.node
            children = deque()
            for child_node in self.tree.expand(self.problem, parent):
                if child_node.state not in self.visited:
                    children.append(child_node)# ?? what is children
                    self.visited.add(child_node.state)
            children.extend(self.frontier) # ??
            self.frontier = children# ??
        return None