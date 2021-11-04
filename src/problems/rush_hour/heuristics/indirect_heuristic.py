from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.rush_hour import RushHourProblem
from problems.rush_hour.vehicle import Orientation, RushHourVehicle

from base import Heuristic


class RushHourIndirectHeuristic(Heuristic[RushHourBoard]):
    def __init__(self, problem: RushHourProblem) -> None:
        super().__init__(problem)

    def __call__(self, board: RushHourBoard) -> float:
        def optimistic_unblock(v: RushHourVehicle, ty: int) -> int:  
            top_border = 0
            bot_border = board.shape[0]
            top_blocking_vhs = [v2 for v2 in board.vehicles if
                                v2.y < v.y 
                                and v2.x <= v.x 
                                and v2.xEnd >= v.x]
            bot_blocking_vhs = [v2 for v2 in board.vehicles if
                                v2.y > v.yEnd 
                                and v2.x <= v.x 
                                and v2.xEnd >= v.x]
            top_border += sum((v2.length for v2 in top_blocking_vhs if v2.orientation == Orientation.VERTICAL))
            bot_border -= sum((v2.length for v2 in bot_blocking_vhs if v2.orientation == Orientation.VERTICAL))
            to_top = v.yEnd - ty - 1 if v.length + top_border < ty else board.shape[0]
            to_bot = ty - v.y + 1 if bot_border - v.length > ty else board.shape[0]
            to_top += len(top_blocking_vhs)
            to_bot += len(bot_blocking_vhs)
            return min(to_top, to_bot)

        target_vehicle = [v for v in board.vehicles if v.id == 'X'][0]
        if target_vehicle.x == 4:
            return 0
        blocking_vehicles = [v for v in board.vehicles 
                             if v.orientation == Orientation.VERTICAL 
                                and v.x > target_vehicle.xEnd 
                                and v.y <= target_vehicle.y 
                                and v.yEnd >= target_vehicle.y]
        moves_to_unblock = sum([optimistic_unblock(v, target_vehicle.y) for v in blocking_vehicles])
        distance = board.shape[1] - (target_vehicle.xEnd)
        return moves_to_unblock + distance
