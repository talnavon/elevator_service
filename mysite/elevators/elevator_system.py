from time import sleep
import timeit

from .elevator import Elevator


class ElevatorSystem:
    """A system for managing a building's elevators.
    Takes floor and elevator count as parameters.init will create the necessary Elevator objects.
    Active elevators are held on floors and accessed there."""
    __instance = None

    @staticmethod
    def get_instance():

        if ElevatorSystem.__instance is None:
            ElevatorSystem()
        return ElevatorSystem.__instance

    def __init__(self, floor_count=50, elevator_count=4):
        if ElevatorSystem.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            ElevatorSystem.__instance = self
        if floor_count < 2 or elevator_count < 2:
            raise (ValueError, "Invalid parameters"
                   "Floor and elevator counts should be greater than 1.")

        self.elevators = [Elevator(i) for i in range(elevator_count)]
        self.floors = [[] for _ in range(floor_count)]
        self.floors[0] = self.elevators[:]
        self.start = timeit.default_timer()

    def __repr__(self):
        return ("<ElevatorSystem object containing {} floors and {} elevators>"
                .format(len(self.floors), len(self.elevators)))

    def __str__(self):
        return ("Elevator System with {} elevators on floors "
                .format(len(self.elevators)) +
                ', '.join(str(elevator.floor if elevator.floor else 'G')
                          for elevator in self.elevators))

    def validate_floor(self, floor):
        """Raises a ValueError if floor doesn't exist."""

        if floor >= len(self.floors):
            raise ValueError("Invalid floor {}, system only "
                             "has {} floors.".format(floor, len(self.floors)))

    def choose_elevator(self, elevators, direction):
        """Return elevator that's most suitable.

        Takes in direction to first filter out moving elevators.
        Alternatively filters out elevators moving the wrong direction.
        Lastly will take the least worn elevator as its choice."""

        # First try take static elevators
        chosen_elevators = [elevator for elevator in elevators if
                            elevator.direction is None]

        # Now get elevators travelling in the right direction
        if not chosen_elevators:
            chosen_elevators = [elevator for elevator in elevators if
                                elevator.direction == direction]

        # If that fails too, just take what we've got
        if not chosen_elevators:
            chosen_elevators = elevators

        # Sort by where and take the first ie. lowest value in the sorted list
        return sorted(chosen_elevators, key=lambda ele: ele.where)[0]

    def call_elevator(self, floor, direction):
        """Chooses and returns an elevator after moving it to floor.

        Floor should be the floor the elevator is called to.
        Direction should indicate which way the user wants to travel.
        Valid values are 1 or -1."""

        self.start = timeit.default_timer()
        self.validate_floor(floor)
        if direction not in (1, -1):
            raise ValueError("direction only accepts 1 or -1, not {}".
                             format(direction))

        # Check if there's any elevators on the current floor
        if self.floors[floor]:
            elevator = self.choose_elevator(self.floors[floor], direction)
            elevator.open()
            return elevator

        # Now search outward, one floor up and down at a time.
        # None pads the list if we run out of floors in one direction

        check_floors = map(lambda x, y: (x, y), range(floor + 1, len(self.floors)),
                           range(floor - 1, -1, -1))
        for up, down in check_floors:
            if down is not None and self.floors[down]:
                elevator = self.choose_elevator(self.floors[down], direction)
                break
            if up is not None and self.floors[up]:
                elevator = self.choose_elevator(self.floors[up], direction)
                break
        else:
            raise Exception("Cannot find elevators.")

        # self.move_elevator(elevator, floor)
        return elevator

    def move_elevator(self, elevator, floor):
        """Send elevator to floor, moving one floor at a time."""

        self.validate_floor(floor)
        print("Elevator {} moving".format(elevator.name))

        move_up = elevator.floor < floor
        elevator.direction = 1 if move_up else -1

        # Build the range based on which direction we need to go
        # We do this because range won't work if floor < elevator.floor
        for _ in (range(elevator.floor, floor) if move_up
                            else range(elevator.floor, floor, -1)):
            elevator.move(self)
            sleep(2)

        sleep(10)
        stop = timeit.default_timer()
        print('Time: ', stop - self.start)
        elevator.open()
        elevator.direction = None


# if __name__ == '__main__':
#
#     es = ElevatorSystem(floor_count=50, elevator_count=4)
#     es.call_elevator(floor=12, direction=1)
#     es.call_elevator(floor=10, direction=-1)








