from base import Problem
from problems.rush_hour.vehicle import RushHourVehicle, Orientation
from problems.rush_hour.board import RushHourBoard
from typing import Set, Tuple
from copy import deepcopy
from enum import Enum


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class RushHourProblem(Problem):
    def __init__(self, vehicles: Set[RushHourVehicle], initial: RushHourBoard, goal: RushHourVehicle = RushHourVehicle('X', 4, 2, 'H')):
        super().__init__(initial, goal)
        self.vehicles = vehicles


    def actions(self, board: RushHourBoard):
        actions = []

        shifts = {
            Orientation.VERTICAL.value: [(Direction.UP, -1, 0), (Direction.DOWN, 1, 0)],
            Orientation.HORIZONTAL.value: [(Direction.LEFT, 0, -1), (Direction.RIGHT, 0, 1)]
        }

        matrix = board.get_board()
        for vehicle in board.vehicles:
            for shift, y, x in shifts[vehicle.orientation]:
                if self.on_board(vehicle.x+x, vehicle.y+y) and (shift == Direction.UP or Direction.LEFT):
                    if matrix[vehicle.y+y, vehicle.x+x] == ' ':
                        actions.append((shift, vehicle.id))
                if self.on_board(vehicle.xEnd+x, vehicle.yEnd+y) and (shift == Direction.DOWN or Direction.RIGHT):
                    if matrix[vehicle.yEnd+y, vehicle.xEnd+x] == ' ':
                        actions.append((shift, vehicle.id))                    
        return actions


    def transition_model(self, board: RushHourBoard, action: Tuple[Direction, str]) -> RushHourBoard:
        moves = {
            Direction.UP: (-1, 0),
            Direction.DOWN: (1, 0),
            Direction.RIGHT: (0, 1),
            Direction.LEFT: (0, -1)
        }[action[0]]

        for vehicle in board.vehicles:
            if vehicle.id == action[1]:
                y = vehicle.y + moves[0]
                x = vehicle.x + moves[1]
                new_vehicle = RushHourVehicle(vehicle.id, x, y, vehicle.orientation)
                new_vehicles = deepcopy(board.vehicles)
                new_vehicles.remove(vehicle)
                new_vehicles.add(new_vehicle)
                new_board = RushHourBoard(new_vehicles)
        return new_board


    def action_cost(self, board: RushHourBoard, action: Tuple[Direction, str], new_board: RushHourBoard):
        return 1


    def is_goal(self, board: RushHourBoard) -> bool:
        return self.goal in board.vehicles


    def on_board(self, x: int, y: int) -> bool:
        board = self.initial.get_board()
        return 0 <= x < board.shape[1] and 0 <= y < board.shape[0]
