from enum import Enum


class Color(Enum):
    WHITE = 1
    GREY = 2
    BLACK = 3


class Type(Enum):
    NODE = 0
    WALL = 1


class Node:
    def __init__(self, x, y):
        self.parent = None
        self.child = None
        self.visited = False
        self.d = float('inf')  # path cost (gold?)
        self.type = Type.NODE  # 0 = node, 1 = wall
        self.x = x
        self.y = y
        self.color = Color.WHITE
        self.h = None
        self.f = None