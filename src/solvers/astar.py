from src.tree import Node, Tree
from src.solvers.best_first import BestFirstSearch
from src.solvers.utils import Heap


class AStar(BestFirstSearch):
    def __init__(self, problem, state, heuristic):
        super().__init__(problem, state)
        self.frontier = Heap(maxheap=False, key=lambda x: x.cost + heuristic(x.state))
        
        
    

