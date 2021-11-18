from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, TypeVar
from base.heuristic import Heuristic
from base.problem import ReversibleProblem, Problem
from tree.node import Node
from tree.tree import Tree


"""
Type variables for the sake of the generic types.
- P: any Problem
- B: any ReversibleProblem
- H: any Heuristic
"""
P = TypeVar('P', bound=Problem)
B = TypeVar('B', bound=ReversibleProblem)
H = TypeVar('H', bound=Heuristic)


class Solver(ABC, Generic[P]):
    """
    An interface for the most generic state space solver. Doesn't use any extra information into consideration.
    It's a generic type depending on the type of the problem.

    Attributes:
    ==========
    problem: P 
        a problem to be solved, it's set up in the __init__

    Abstract Methods:
    =================
    solve() -> Optional[Node]:
        returns the leaf node of the search branch, that leads to solution
    search_tree() -> Tree;
        return a search tree that may be used to monitor the solving process
    """

    def __init__(self, problem: P):
        self.problem = problem

    @abstractmethod
    def solve(self) -> Optional[Node]:
        """ returns the leaf node of the search branch, that leads to solution """

    @abstractmethod
    def search_tree(self) -> Tree:
        """ return a search tree that may be used to monitor the solving process """


class HeuristicSolver(Solver[P], ABC, Generic[P, H]):
    """
    Works same as :class:`Solver`, but uses a heuristic function 
    to guide the search process.

    Attributes: 
    ==========
        problem: P
            inherited from the :class:`Solver`
        heuristic: H
            a heuristic used to guide the search, set up in the constructor
    """

    def __init__(self, problem: P, heuristic: H):
        super().__init__(problem)
        self.heuristic = heuristic


class BidirectionalHeuristicSolver(Solver[B], ABC, Generic[B, H]):
    """
    Works same as :class:`Solver`, but uses a heuristic function 
    to guide the search process in two directions simultaneously.

    It can be used only on the reversible problems.

    Attributes: 
    ==========
        problem: B
            inherited from the :class:`Solver`, it's restricted to the reversible problems
        primary_heuristic: H
            a heuristic used to guide the search in the primary (initial -> goal) direction
            set up in the __init__
        opposite_heuristic: H
            a heuristic used to guide the search in the opposite (goal -> initial) direction
            set up in the __init__
    """

    def __init__(self, problem: B, primary_heuristic: H, opposite_heuristic: H):
        super().__init__(problem)
        self.primary_heuristic = primary_heuristic
        self.opposite_heuristic = opposite_heuristic
