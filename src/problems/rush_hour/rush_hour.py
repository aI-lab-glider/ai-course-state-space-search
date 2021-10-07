from base import Problem
from problems.rush_hour.vehicle import RushHourVehicle
from problems.rush_hour.board import RushHourBoard
from copy import deepcopy


class RushHourProblem(Problem):
    def __init__(self, vehicles, initial: RushHourBoard, goal = RushHourVehicle('X', 4, 2, 'H')):
        super().__init__(goal)
        self.vehicles = vehicles
        self.initial = initial.get_board()


    def actions(self, board: RushHourBoard):
        actions = []

        shifts = {
            'V': [('up', -1, 0), ('down', 1, 0)],
            'H': [('left', 0, -1), ('right', 0, 1)]
        }

        matrix = board.get_board()
        for vehicle in board.vehicles:
            for shift, y, x in shifts[vehicle.orientation]:
                if self.on_board(vehicle.x+x, vehicle.y+y) and (shift == 'up' or 'left'):
                    if matrix[vehicle.y+y, vehicle.x+x] == ' ':
                        actions.append((shift, vehicle.id))
                if self.on_board(vehicle.xEnd+x, vehicle.yEnd+y) and (shift == 'down' or 'right'):
                    if matrix[vehicle.yEnd+y, vehicle.xEnd+x] == ' ':
                        actions.append((shift, vehicle.id))                    
        return actions


    def transition_model(self, board: RushHourBoard, action):
        move = {
            "up": (-1, 0),
            "down": (1, 0),
            "right": (0, 1),
            "left": (0, -1)
        }[action[0]]

        for vehicle in board.vehicles:
            if vehicle.id == action[1]:
                y = vehicle.y + move[0]
                x = vehicle.x + move[1]
                new_vehicle = RushHourVehicle(vehicle.id, x, y, vehicle.orientation)
                new_vehicles = deepcopy(board.vehicles)
                new_vehicles.remove(vehicle)
                new_vehicles.add(new_vehicle)
                new_board = RushHourBoard(new_vehicles)
         
        return new_board


    def action_cost(self, board: RushHourBoard, action, new_board: RushHourBoard):
        return 1


    def is_goal(self, board: RushHourBoard):
        board = board.get_board()
        return board[2,5] == 'X'


    def on_board(self, x: int, y: int) -> bool:
        yEnd, xEnd = self.initial.shape
        return 0 <= x < xEnd and 0 <= y < yEnd