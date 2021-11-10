from __future__ import annotations
from enum import Enum

from base import State
from typing import Tuple, Union, cast
from numpy.typing import NDArray
from dataclasses import dataclass


class GridCell(Enum):
    EMPTY = " "
    WALL = "#"


@dataclass(eq=True)
class GridCoord(State):
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __add__(self, other: Union[GridCoord, Tuple[int, int]]) -> GridCoord:
        shift_y, shift_x = other
        return GridCoord(self.x + shift_x, self.y + shift_y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __iter__(self):
        return iter((self.y, self.x))


@dataclass(frozen=True)
class Grid:
    board: NDArray

    def get_cell(self, c: GridCoord) -> GridCell:
        return cast(GridCell, self.board[c.y, c.x])

    @property
    def shape(self) -> Tuple[int, int]:
        return cast(Tuple[int, int], self.board.shape)
    
    def __iter__(self):
        return iter(self.board)

    def __getitem__(self, key):
        return self.board[key]