from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Generator, Generic, List, TypeVar
from base.problem import Problem
from base.state import State
from tree import Node


"""
Type variable used in the generics
- S: any State
"""
S = TypeVar("S", bound=State)


class NodeEvent(Enum):
    """
    This enum represents all possible events sent by the Tree
    - Closed: algorithm has expanded the node
    - Opened: algorithm got access to the node
    """
    Closed = auto()
    Opened = auto()


class NodeEventSubscriber(ABC, Generic[S]):
    """
    Interface responsible for monitoring the search process.

    Abstract methods:
    =================
    got_event(node: Node[S], event: NodeEvent) -> None:
        this method is called when the search tree is expanded
        contains info about the node and type of the event
    """

    @abstractmethod
    def got_event(self, node: Node[S], event: NodeEvent) -> None:
        """
        this method is called when the search tree is expanded
        contains info about the node and type of the event
        """


class Tree(Generic[S]):
    """
    This class represents the search tree expanded by the algorithm.
    It informs interested subscribers about the search process.

    Attributes:
    ===========
    root: Node[S]
        root of the tree
        set up in the __init__
    subscribers: List[NodeEventSubscriber[S]]
        objects notified by the tree about the search progress
        updated by subscribe method

    Methods:
    ========
    subscribe(subscriber: NodeEventSubscriber[S]) -> None
        registers a new subscriber
    expand(problem: problem[S, Any], node: Node[S]) -> Generator[Node[S], None, None]:
        allows to iterate over all the possible children of the given node
    """
    def __init__(self, root: Node[S]):
        self.root = root
        self.subscribers : List[NodeEventSubscriber[S]] = []


    def subscribe(self, subscriber: NodeEventSubscriber[S]) -> None:
        
        self.subscribers.append(subscriber)

    def _notify(self, node: Node[S], event: NodeEvent) -> None:
        """Notify subscriber about new node event"""
        for subscriber in self.subscribers:
            subscriber.got_event(node, event)


    def expand(self, problem: Problem[S, Any], node: Node[S]) -> Generator[Node[S], None, None]:
        self._notify(node, NodeEvent.Closed)
        for action in problem.actions(node.state):
            child_state = problem.take_action(node.state, action)
            child_node = Node(
                state=child_state, 
                parent=node,
                cost=node.cost + problem.action_cost(node.state, action),
                action=action
                )

            self._notify(child_node, NodeEvent.Opened)
            yield child_node


