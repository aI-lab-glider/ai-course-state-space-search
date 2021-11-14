from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, TypeVar
from base.heuristic import Heuristic
from base.problem import Problem
from tree.node import Node
from tree.tree import Tree

P = TypeVar('P', bound=Problem)
H = TypeVar('H', bound=Heuristic)


class Solver(ABC, Generic[P]):
    """
    Solves for which it was created by searching its search tree.
    """

    def __init__(self, problem: P):
        self.problem = problem

    @abstractmethod
    def solve(self) -> Optional[Node]:
        """
        Solves problem for which solver was created.
        """

    @abstractmethod
    def search_tree(self) -> Tree:
        """
        Returns tree that was created during search.
        """


class HeuristicSolver(Solver[P], ABC, Generic[P, H]):
    """
    Works same as :class:`Solver`, but instead of searching full tree, 
    it applies heuristic to reduce number of nodes to search.

    Args: 
        problem: problem, states of which can be representet as tree
        heuristic: function to estimate if state should be epxanded
    """

    def __init__(self, problem: P, heuristic: H):
        super().__init__(problem)
        self.heuristic = heuristic
