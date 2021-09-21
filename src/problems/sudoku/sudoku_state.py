from base import State
from typing import List, Union
import numpy as np

class SudokuState(State):
    def __init__(self, matrix: List[List[int]]):
        self.matrix = matrix
        self.dx = len(matrix)
        self.dy = len(matrix[0])


    def __hash__(self):
        pass


    def __eq__(self, other):
        return hash(self) == hash(other)


    def __str__(self) -> str:
        return str(np.matrix)


    def display(self) -> str:
        pass
