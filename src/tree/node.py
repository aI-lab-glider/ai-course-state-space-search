import numpy as np


class Node:
    def __init__(self, state, parent=None, action=None, cost=np.inf):
        self.state = state
        self.cost = cost
        self.parent = parent
        self.action = action
        self.children = set()

    
    def __lt__(self, other):
        return self.cost < other.cost


    def add_child(self, child):
        self.children.add(child)

