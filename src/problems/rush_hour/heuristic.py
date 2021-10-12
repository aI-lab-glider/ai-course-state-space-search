from problems.rush_hour.board import RushHourBoard

class RushHourHeuristic:

    def blocking_cars(self, board: RushHourBoard):
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        if target_vehicle.x == 4:
            return 0
        blockingcars = 1
        for vehicle in board.vehicles:
            if vehicle.orientation == 'V' and vehicle.x > target_vehicle.xEnd and (vehicle.y <= target_vehicle.y and vehicle.yEnd >= target_vehicle.y):
                blockingcars += 1
        return blockingcars


    def distance_to_exit(self, board: RushHourBoard):
        target_vehicle = [vehicle for vehicle in board.vehicles if vehicle.id == 'X'][0]
        distance = 5 - (target_vehicle.xEnd)
        return distance
