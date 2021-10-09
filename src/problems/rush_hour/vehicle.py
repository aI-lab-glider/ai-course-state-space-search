from base import State
from typing import Union


CAR_ID = ('X', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K')
TRUCK_ID = ('O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'Z')


class RushHourVehicle(State):
    def __init__(self, id: str, x: int, y: int, orientation: str):
        self.id = id
        self.x = x
        self.y = y
        self.orientation = orientation

        if id in CAR_ID: 
            self.length = 2
        else: 
            self.length = 3

        if orientation == "H": 
            self.xEnd = x + self.length - 1
            self.yEnd = self.y
        else: 
            self.xEnd = self.x
            self.yEnd = y + self.length - 1  

        assert id in CAR_ID or id in TRUCK_ID, "Vehicle id must be a single capital letter"
        assert (self.x >= 0 and self.y >= 0 and self.xEnd < 6 and self.yEnd < 6), f"Vehicle {self.id} moves off the board"


    def __hash__(self):
        return hash(self.id)


    def __eq__(self, other):
        return hash(self) == hash(other)


    def __str__(self) -> str:
        return str(self.id)


    def display(self):
        print("Vehicle: {}, {}, {}, {}".format(self.id, self.x, self.y, self.orientation))
