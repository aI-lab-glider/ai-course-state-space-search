from base import State
from typing import List


class NPuzzleState(State):
    def __init__(self, matrix: List[List[int]], x: int, y: int):
        super().__init__()
        self.matrix = matrix
        self.x = x
        self.y = y
        self.nx = len(self.matrix)
        self.ny = len(self.matrix[0])

    def __hash__(self):
        return hash(tuple([tuple(l) for l in self.matrix]))

    def __str__(self) -> str:
        s = "\n"
        for i in range(self.nx):
            for j in range(self.ny):
                if j == self.ny - 1:
                    s += ''.join(f"{self.matrix[i][j]}\n")
                else:
                    s += ''.join(f"{self.matrix[i][j]} ")
        return s

    def __eq__(self, other):
        return self.matrix == other.matrix
