from base import Heuristic
from problems.route_finding.route_finding import RouteFinding
from problems.route_finding.location import Location
import numpy as np


class RouteFindingHeuristic(Heuristic):
 
    def __init__(self, problem: RouteFinding):
        self.problem = problem


    def apply(self, location: Location) -> float:
        distance = np.linalg.norm(np.array(location.coord) - np.array(self.problem.goal.coord), ord=np.inf)
        return distance