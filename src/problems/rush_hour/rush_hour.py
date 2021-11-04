from __future__ import annotations
from base import Problem
from problems.rush_hour.vehicle import RushHourVehicle, Orientation
from problems.rush_hour.board import RushHourBoard
from problems.rush_hour.rush_hour_action import Direction, VehicleShift
from typing import Set, List, Dict, Tuple, cast
from copy import deepcopy
from enum import Enum
import numpy as np
from PIL import Image, ImageDraw


class RushHourProblem(Problem[RushHourBoard, VehicleShift]):
    def __init__(self, vehicles: Set[RushHourVehicle], initial: RushHourBoard, goal: RushHourVehicle = RushHourVehicle('X', 4, 2, Orientation.HORIZONTAL)):
        super().__init__(initial)
        self.goal = goal
        self.vehicles = vehicles


    def actions(self, board: RushHourBoard) -> List[VehicleShift]:

        shifts = {
            Orientation.VERTICAL: [Direction.UP, Direction.DOWN],
            Orientation.HORIZONTAL: [Direction.LEFT, Direction.RIGHT]
        }

        matrix = board.get_board()
        actions = [VehicleShift(shift, vehicle.id)
                   for vehicle in board.vehicles 
                   for shift in shifts[vehicle.orientation]
                   if self.is_valid_move(matrix, vehicle, shift)]
        return actions


    def take_action(self, board: RushHourBoard, action: VehicleShift) -> RushHourBoard:
        for vehicle in board.vehicles:
            if vehicle.id == action.vehicle_id:
                y = vehicle.y + action.shift.value[0]
                x = vehicle.x + action.shift.value[1]
                new_vehicle = RushHourVehicle(vehicle.id, x, y, vehicle.orientation, vehicle.length)
                new_vehicles = deepcopy(board.vehicles)
                new_vehicles.remove(vehicle)
                new_vehicles.add(new_vehicle)
                new_board = RushHourBoard(new_vehicles, board.shape)
        return new_board


    def action_cost(self, board: RushHourBoard, action: VehicleShift, new_board: RushHourBoard) -> float:
        return 1


    def is_goal(self, board: RushHourBoard) -> bool:
        return self.goal in board.vehicles


    def on_board(self, x: int, y: int) -> bool:
        board = self.initial.get_board()
        return 0 <= x < board.shape[1] and 0 <= y < board.shape[0]


    def is_valid_move(self, matrix, vehicle: RushHourVehicle, shift: Direction):
        y, x = shift.value
        if self.on_board(vehicle.x+x, vehicle.y+y) and (shift == Direction.UP or Direction.LEFT) and matrix[vehicle.y+y, vehicle.x+x] == ' ':
            return True
        if self.on_board(vehicle.xEnd+x, vehicle.yEnd+y) and (shift == Direction.DOWN or Direction.RIGHT) and matrix[vehicle.yEnd+y, vehicle.xEnd+x] == ' ':
            return True  
        return False

    def to_image(self, board: RushHourBoard, size: Tuple[int, int] = (800, 800)) -> Image.Image:
        background_color = (248, 255, 229)
        image = Image.new("RGB", size, background_color)
        draw = ImageDraw.Draw(image)
        grid_width = int(image.width / board.shape[1])
        grid_height = int(image.height / board.shape[0])
        border = int(grid_width / 10)

        for x in range(0, image.width, grid_width):
            line = ((x, 0), (x, image.height))
            draw.line(line, fill="black")

        for y in range(0, image.height, grid_height):
            line = ((0, y), (image.width, y))
            draw.line(line, fill="black")

        def get_color(vehicle_id):
            red = (196, 40, 71)
            blue = (31, 122, 140)
            if vehicle_id == "X":
                return red
            return blue

        for v in board.vehicles:
            x_start = v.x * grid_width + border
            y_start = v.y * grid_height + border
            x_end = (v.xEnd + 1) * grid_width - border
            y_end = (v.yEnd + 1) * grid_height - border
            draw.rectangle((x_start, y_start, x_end, y_end), get_color(v.id))

        return image

    @staticmethod
    def deserialize(text: str) -> RushHourProblem:
        lines = text.splitlines()
        raw_board = []
        for l in lines:
            if l.startswith("|"):
                raw_board.append(list(l.strip().replace("|", "").upper()))

        width = max((len(r) for r in raw_board))
        for r in raw_board:
            if len(r) < width:
                r += [' '] * (width - len(r))

        board = np.array(raw_board)

        vehicles: Dict[str, RushHourVehicle] = dict()
        height, width = board.shape
        for x in range(width):
            for y in range(height):
                v = board[y,x]
                if v == ' ' or v in vehicles:
                    continue

                rx = [r for r in range(x, width) 
                              if board[y,r] == v]

                if len(rx) > 1:
                    vehicles[v] = RushHourVehicle(v, x, y, Orientation.HORIZONTAL, len(rx))
                    continue

                dy = [d for d in range(y, height) 
                              if board[d,x] == v]
                vehicles[v] = RushHourVehicle(v, x, y, Orientation.VERTICAL, len(dy))
        
        
        initial_vehicles = set(vehicles.values())
        initial = RushHourBoard(initial_vehicles, cast(Tuple[int,int], board.shape))
        goal = deepcopy(vehicles["X"])
        goal.x = width - vehicles["X"].length

        return RushHourProblem(initial_vehicles, initial, goal)
                    
