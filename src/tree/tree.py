from tree import Node
from typing import Callable
import pydot


class Tree:
    def __init__(self, root):
        self.root = root
        self.subscribers = []
        self.visit_counter = 0


    def subsribe(self, subscriber):
        """Add new subscriber to the list"""
        self.subscribers.append(subscriber)


    def _notify(self, node):
        """Notify subscriber about new node event"""
        for subscriber in self.subscribers:
            subscriber.update(node)     # append but better?


    def expand(self, problem, node):
        """Generator over child nodes"""
        self.visit_counter += 1
        node.visit_time = self.visit_counter
        for action in problem.actions(node.state):
            child_state = problem.transition_model(node.state, action)
            action_cost =  problem.action_cost(node.state, action, child_state)
            child_node = Node(
                state=child_state, 
                parent=node,
                cost=node.cost + action_cost,
                action=action
                )
            node.add_child(child_node)
            self._notify(child_node)
            yield child_node


    def as_image(self, save_path: str):
        def add_node(node, graph):
            v = pydot.Node(hash(node), label=f"state: {node.state}\ncost:{node.cost}\ntime:{node.visit_time}")
            graph.add_node(v)
            if node.parent:
                e = pydot.Edge(hash(node.parent), hash(node), label=f"action:{node.action}\ncost:{node.cost - node.parent.cost}")
                graph.add_edge(e)
        graph = pydot.Dot(graph_type="digraph")
        self.traverse(lambda n: add_node(n, graph))
        graph.write_png(save_path)


    
    def traverse(self, fun: Callable[[Node], None]) -> None:
        """traverse the tree and call given fun on every node"""
        def _traverse(node):
            for child in node.children:
                fun(child)
                _traverse(child)
        _traverse(self.root)
    




