from problems.rush_hour.board import RushHourBoard
from base import Heuristic


class DistanceToExitHeuristic(Heuristic):

    def apply(self, board: RushHourBoard) -> int:
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        distance = 5 - (target_vehicle.xEnd)
        return distance
