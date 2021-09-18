from base import State

class NPuzzleState(State):
    def __init__(self, matrix, x, y):
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


    def __str__(self):
        """ dobrze to? """
        return str(self.matrix)

    
    def display(self):
        """ nw co tu trzeba"""
        return str(self.matrix)