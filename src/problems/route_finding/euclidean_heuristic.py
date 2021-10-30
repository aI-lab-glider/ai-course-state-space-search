from base import Heuristic
from problems.route_finding.route_finding import RouteFinding
from problems.route_finding.location import Location
from math import sqrt


class RouteFindingEuclideanHeuristic(Heuristic):
 
    def __init__(self, problem: RouteFinding):
        self.problem = problem


    def apply(self, location: Location) -> float:
        distance = sqrt((location.coord[0] - self.problem.goal.coord[0])**2 + (location.coord[1] - self.problem.goal.coord[1])**2 )
        return distance
