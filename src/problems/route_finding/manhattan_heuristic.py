from base import Heuristic
from problems.route_finding.route_finding import RouteFinding
from problems.route_finding.location import Location


class RouteFindingManhattanHeuristic(Heuristic):
 
    def __init__(self, problem: RouteFinding):
        self.problem = problem


    def apply(self, location: Location) -> float:
        distance = abs(location.coord[0] - self.problem.goal.coord[0]) + abs(abs(location.coord[1] - self.problem.goal.coord[1]))
        return distance
