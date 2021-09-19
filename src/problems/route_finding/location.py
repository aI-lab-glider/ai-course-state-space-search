from base import State
from typing import Tuple, Union


# TODO: add @property for id and coord
class Location(State):
    def __init__(self, id: Union[int, str], coordinates: Tuple[int, int]):
        self.id = id    # nazwa miasta
        self.coord = coordinates    # koordynaty na mapie

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __str__(self):
        return str(self.id)

    def display(self):
        print(f"<id: {self.id}, coord: {self.coord}>")




