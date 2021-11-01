from problems.rush_hour.board import RushHourBoard
from base import Heuristic


class DistanceToExitHeuristic(Heuristic[RushHourBoard]):

    def __call__(self, board: RushHourBoard) -> float:
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        distance = 5 - (target_vehicle.xEnd)
        return distance
