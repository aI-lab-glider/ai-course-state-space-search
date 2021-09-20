from base import State
from typing import List


class NPuzzleState(State):
    def __init__(self, matrix: List[List], x: int, y: int):
        super().__init__()
        self.matrix = matrix
        self.x = x
        self.y = y
        self.nx = len(self.matrix)
        self.ny = len(self.matrix[0])
    
    def __hash__(self):
        tmp = [0] * self.nx
        for i in range(self.nx):
            tmp[i] = tuple(self.matrix[i])
        return hash(tuple(tmp))


    def __str__(self) -> str:
        s = "\n"
        for i in range(self.nx):
            for j in range(self.ny):
                if j == self.ny - 1:
                    s += ''.join(f"{self.matrix[i][j]}\n")
                else:
                    s += ''.join(f"{self.matrix[i][j]} ")
        # s += ''.join("~~"*self.ny + "\n")
        return s

    
    def display(self) -> str:
        print(f"void coordinates: {self.x} {self.y}")
    
    def __eq__(self, other):
        return hash(self) == hash(other)