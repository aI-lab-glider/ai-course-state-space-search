class Node:
    def __init__(self, state, parent=None):
        self.state = state  # np. NPuzzleState, który ma w sobie matrix
        self.parent = parent
        self.children = set()

        self.g = float('inf')
        self.action


    def add_child(self, child):
        self.children.add(child)

