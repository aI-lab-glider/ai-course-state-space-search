from __future__ import annotations
from enum import Enum
from typing import Sequence, Tuple, Set


class GridMove(Enum):
    N = (-1, 0)
    S = (1, 0)
    W = (0, -1)
    E = (0, 1)
    NW = (-1, -1)
    NE = (-1, 1)
    SW = (1, -1)
    SE = (1, 1)

    @staticmethod
    def from_value(value: Tuple[int,int]) -> GridMove:
        return {
            (-1, 0): GridMove.N,
            (1, 0): GridMove.S,
            (0, -1): GridMove.W,
            (0, 1): GridMove.E,
            (-1, -1): GridMove.NW,
            (-1, 1): GridMove.NE,
            (1, -1): GridMove.SW,
            (1, 1): GridMove.SE,
        }[value]

    @staticmethod
    def diagonal_moves() -> Set[GridMove]:
        return {GridMove.NW, GridMove.NE, GridMove.SW, GridMove.SE}

    def involved_moves(self) -> Sequence[GridMove]:
        if self not in GridMove.diagonal_moves():
            return [self]
        shift_l = (0, self.value[1])
        shift_r = (self.value[0], 0)
        return [self, GridMove.from_value(shift_l), GridMove.from_value(shift_r)] 

    def __str__(self) -> str:
        return self.name