import numpy as np


class Node:
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.children = set()


        self.action = action
        self.cost = cost

    
    def __lt__(self, other):
        return self.cost < other.cost

    
    def __str__(self):
        return str(self.state)

    
    def __repr__(self):
        return f"<{str(self.parent)} --{self.action}--> {str(self.state)}. cost: {self.cost}>"


    def path(self):
        node, path = self, []
        while node:
            path.append(node)
            node = node.parent
        return path[::-1]


    def add_child(self, child):
        self.children.add(child)

