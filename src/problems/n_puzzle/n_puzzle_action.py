from enum import Enum


class NPuzzleAction(Enum):
    Right = (0, 1)
    Left = (0, -1)
    Up = (-1, 0)
    Down = (1, 0) 