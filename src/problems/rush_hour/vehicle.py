from base import State


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

    def __hash__(self):
        return hash(self.__str__())


    def __eq__(self, other):
        return self.__dict__ == other.__dict__


    def __str__(self) -> str:
        return "Vehicle: {}, {}, {}, {}".format(self.id, self.x, self.y, self.orientation)


    def display(self):
        print("Vehicle: {}, {}, {}, {}".format(self.id, self.x, self.y, self.orientation))
