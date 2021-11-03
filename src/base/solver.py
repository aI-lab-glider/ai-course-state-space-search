from abc import ABC, abstractmethod
from typing import Callable, Generic, Optional, TypeVar
from base.heuristic import Heuristic
from base.problem import Problem
from tree.node import Node
from tree.tree import Tree

P = TypeVar('P', bound=Problem)
H = TypeVar('H', bound=Heuristic)

class Solver(ABC, Generic[P]):
    def __init__(self, problem: P):
        self.problem = problem

    @abstractmethod
    def solve(self) -> Optional[Node]:
        raise NotImplementedError

    @abstractmethod
    def search_tree(self) -> Tree:
        raise NotImplementedError
        

class HeuristicSolver(Solver[P], ABC, Generic[P,H]):
    def __init__(self, problem: P, heuristic: H):
        super().__init__(problem)
        self.heuristic = heuristic
