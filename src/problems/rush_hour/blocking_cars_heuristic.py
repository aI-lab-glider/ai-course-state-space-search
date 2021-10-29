from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.vehicle import Orientation
from base import Heuristic


class BlockingCarsHeuristic(Heuristic):

    def apply(self, board: RushHourBoard) -> int:
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        if target_vehicle.x == 4:
            return 0
        blockingcars = 1
        for vehicle in board.vehicles:
            if vehicle.orientation == Orientation.VERTICAL and vehicle.x > target_vehicle.xEnd and vehicle.y <= target_vehicle.y and vehicle.yEnd >= target_vehicle.y:
                blockingcars += 1
        return blockingcars
