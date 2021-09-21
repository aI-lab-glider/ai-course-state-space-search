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
            subscriber.update(node)


    def expand(self, problem, node):
        """Generator over child nodes"""
        for action in problem.actions(node.state):
            child_state = problem.transition_model(node.state, action)
            child_node = Node(
                state=child_state, 
                parent=node,
                cost=node.cost + problem.action_cost(node.state, action, child_state),
                action=action
                )
            node.add_child(child_node)
            self._notify(child_node)
            yield child_node


