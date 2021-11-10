from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import List
from tree import Node


class NodeEvent(Enum):
    Closed = auto()
    Opened = auto()


class NodeEventSubscriber(ABC):

    @abstractmethod
    def got_event(self, node: Node, event: NodeEvent) -> None:
        pass


class Tree:
    def __init__(self, root):
        self.root = root
        self.subscribers : List[NodeEventSubscriber] = []


    def subscribe(self, subscriber: NodeEventSubscriber):
        """Add new subscriber to the list"""
        self.subscribers.append(subscriber)


    def _notify(self, node: Node, event: NodeEvent):
        """Notify subscriber about new node event"""
        for subscriber in self.subscribers:
            subscriber.got_event(node, event)


    def expand(self, problem, node):
        """Generator over child nodes"""
        self._notify(node, NodeEvent.Closed)
        for action in problem.actions(node.state):
            child_state = problem.take_action(node.state, action)
            child_node = Node(
                state=child_state, 
                parent=node,
                cost=node.cost + problem.action_cost(node.state, action, child_state),
                action=action
                )

            self._notify(child_node, NodeEvent.Opened)
            yield child_node


