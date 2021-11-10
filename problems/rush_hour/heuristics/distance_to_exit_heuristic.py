from problems.rush_hour.board import RushHourBoard
from base import Heuristic
from problems.rush_hour.rush_hour import RushHourProblem


class RushHourDistanceToExitHeuristic(Heuristic[RushHourBoard]):
    def __init__(self, problem: RushHourProblem) -> None:
        super().__init__(problem)

    def __call__(self, board: RushHourBoard) -> float:
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        distance = board.shape[1] - (target_vehicle.xEnd)
        return distance
