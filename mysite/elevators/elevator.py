elevator_names = {0: 'a', 1: 'b', 2: 'c', 3: 'd'}


class Elevator:

    def __init__(self, name, floor=0):
        """Takes current floor as a parameter."""

        self.floor = floor
        self.name = name
        self.where = 0
        self.direction = None

    def __str__(self):
        return "Elevator {}".format(elevator_names[self.name])

    def __repr__(self):
        return "<Elevator object {} currently on floor {}>".format(
            self.name, self.floor)

    def open(self):
        print("Doors opening on elevator {}.".format(elevator_names[self.name]))

    def move(self, system):
        """Takes an ElevatorSystem and moves one floor in self.direction."""

        system.floors[self.floor].remove(self)
        self.where += 1
        self.floor += self.direction
        system.floors[self.floor].append(self)

        print("On floor {}...".format(self.floor))

    def get_floor(self):
        return self.floor
