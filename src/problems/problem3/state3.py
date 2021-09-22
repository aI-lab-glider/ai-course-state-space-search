from base import State
from typing import List, Union
import numpy as np

class State3(State):
    def __init__(self):
        pass


    def __hash__(self):
        pass


    def __eq__(self, other):
        return hash(self) == hash(other)


    def __str__(self) -> str:
        return str(np.matrix)


    def display(self):
        pass
