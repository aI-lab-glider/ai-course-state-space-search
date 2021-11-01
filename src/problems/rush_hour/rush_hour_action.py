from enum import Enum
from dataclasses import dataclass


class Direction(Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

@dataclass(eq=True,frozen=True)
class VehicleShift:
    shift: Direction
    vehicle_id: str 
