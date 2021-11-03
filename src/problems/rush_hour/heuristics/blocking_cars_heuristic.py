from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.rush_hour import RushHourProblem
from problems.rush_hour.vehicle import Orientation

from base import Heuristic


class RushHourBlockingCarsHeuristic(Heuristic[RushHourBoard]):
    def __init__(self, problem: RushHourProblem) -> None:
        super().__init__(problem)

    def __call__(self, board: RushHourBoard) -> float:
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        if target_vehicle.x == 4:
            return 0
        blockingcars = 1
        for vehicle in board.vehicles:
            if vehicle.orientation == Orientation.VERTICAL and vehicle.x > target_vehicle.xEnd and vehicle.y <= target_vehicle.y and vehicle.yEnd >= target_vehicle.y:
                blockingcars += 1
        return blockingcars
