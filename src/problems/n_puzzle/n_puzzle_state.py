from base import State
from typing import List


#TODO: Visualize matrix with np module
class NPuzzleState(State):
    def __init__(self, matrix: List[List], x: int, y: int):
        super().__init__()

        # macierz stanu zabawki
        self.matrix = matrix
        # współrzędne zera
        self.x = x
        self.y = y
        self.nx = len(self.matrix)
        self.ny = len(self.matrix[0])
    
    def __hash__(self):
        tmp = [0] * self.nx
        for i in range(self.nx):
            tmp[i] = tuple(self.matrix[i])
        return hash(tuple(tmp))


    '''
    Optional drawning
    '''
    def __str__(self) -> str:
        s = f"\n{self.matrix[0][0]}, {self.matrix[0][1]}, {self.matrix[0][2]},\n{self.matrix[1][0]}, {self.matrix[1][1]}, {self.matrix[1][2]},\n{self.matrix[2][0]}, {self.matrix[2][1]}, {self.matrix[2][2]}"
        return s + "\n~~~~~~"

    
    def display(self) -> str:
        return str(self.matrix)
