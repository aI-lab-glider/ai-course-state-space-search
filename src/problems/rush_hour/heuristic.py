from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.vehicle import Orientation


class RushHourHeuristic:

    def blocking_cars(self, board: RushHourBoard) -> int:
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        if target_vehicle.x == 4:
            return 0
        blockingcars = 1
        for vehicle in board.vehicles:
            if vehicle.orientation == Orientation.VERTICAL and vehicle.x > target_vehicle.xEnd and (vehicle.y <= target_vehicle.y and vehicle.yEnd >= target_vehicle.y):
                blockingcars += 1
        return blockingcars


    def distance_to_exit(self, board: RushHourBoard) -> int:
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        distance = 5 - (target_vehicle.xEnd)
        return distance
