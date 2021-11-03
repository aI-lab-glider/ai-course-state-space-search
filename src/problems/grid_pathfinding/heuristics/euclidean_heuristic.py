from base import Heuristic
from problems.grid_pathfinding.grid_pathfinding import GridPathfinding
from problems.grid_pathfinding.grid import GridCoord
from math import sqrt


class EuclideanHeuristic(Heuristic[GridCoord]):
 
    def __init__(self, problem: GridPathfinding):
        self.problem = problem

    def __call__(self, state: GridCoord) -> float:
        return sqrt((state.x - self.problem.goal.x)**2 + (state.y - self.problem.goal.y)**2)
  
