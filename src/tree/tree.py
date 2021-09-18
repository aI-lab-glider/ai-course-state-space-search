from tree import Node


class Tree:
    def __init__(self, root):
        self.root = root
        self.subscribers = []


    def subsribe(self, subscriber):
        """Add new subscriber to the list"""
        self.subscribers.append(subscriber)


    def _notify(self, node):
        """Notify subscriber about new node event"""
        for subscriber in self.subscribers:
            subscriber.update(node)     # append but better?


    def expand(self, problem, node):
        """Generator over child nodes"""
        for action in problem.actions(node.state):
            child_node = Node(state=problem.transition_model(node.state, action), parent=node)
            node.add_child(child_node)
            self._notify(child_node)
            yield child_node


