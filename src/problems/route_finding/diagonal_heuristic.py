from base import Heuristic
from problems.route_finding.route_finding import RouteFinding
from problems.route_finding.location import Location

import numpy as np


class RouteFindingDiagonalHeuristic(Heuristic[Location]):
 
    def __init__(self, problem: RouteFinding):
        self.problem = problem


    def __call__(self, location: Location) -> float:
        distance = np.maximum(abs(location.coord[0] - self.problem.goal.coord[0]), abs(location.coord[1] - self.problem.goal.coord[1]))
        return distance
