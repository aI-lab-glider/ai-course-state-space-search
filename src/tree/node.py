class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = set()


    def add_child(self, child):
        self.children.add(child)

