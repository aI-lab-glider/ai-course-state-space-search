from src.tree import Node, Tree
from src.solvers.best_first import BestFirstSearch
from src.solvers.utils import Heap


class AStar(BestFirstSearch):
    def __init__(self, problem, state, heuristic):
        super().__init__(problem, state, eval_fun=lambda node: node.cost + heuristic(node.state))
        
        
        
    

