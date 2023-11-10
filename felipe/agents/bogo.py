from agent import VacuumAgent
import random


class BogoVacuum(VacuumAgent):
    """Randomly chooses between:
    - Moving in a random Direction
    - Checking the current square
    - Cleaning the current square
    """

    def act(self):
        action = random.choice(["move", "check", "clean"])

        if action == "move":
            direction = random.choice(["north", "south", "west", "east"])
            self.move(direction)
        elif action == "check":
            self.check()
        elif action == "clean":
            self.clean()


class RandomMovementVacuum(VacuumAgent):
    """Moves in a random direction and then checks if the new square is clean - if not, cleans it."""

    def act(self):
        if len(self.history) == 0 or self.history[-1].startswith("Moved"):
            if not self.check():
                self.clean()
        else:
            direction = random.choice(["north", "south", "west", "east"])
            self.move(direction)


class NoRepeatVacuum(VacuumAgent):
    """Moves in a random direction and then checks if the new square is clean - if not, cleans it.

    Never moves to a square it has already been in.
    """

    def __init__(self, battery=None):
        super().__init__(battery)
        # Initialize memory to store previous positions
        self.memory = set()
        self.memory.add(tuple(self.position))

    def move(self, direction):
        options = ["north", "south", "west", "east"]
        if self.battery is None or self.battery > 0:
            new_position = None

            while len(options) > 0:
                new_position = self.position.copy()
                if direction == "north":
                    new_position[0] -= 1
                elif direction == "south":
                    new_position[0] += 1
                elif direction == "west":
                    new_position[1] -= 1
                elif direction == "east":
                    new_position[1] += 1

                memo = tuple(new_position)
                if memo in self.memory:
                    self.history.append(
                        f"Already moved {direction} - choosing different direction"
                    )
                    options.remove(direction)
                    if len(options) > 0:
                        direction = random.choice(options)
                    continue
                elif self.battery:
                    self.battery -= 1

                self.memory.add(memo)
                break

            if new_position == self.position:
                self.history.append("No possible movements")
            elif (
                0 <= new_position[0] < self.environment.M
                and 0 <= new_position[1] < self.environment.N
            ):
                self.position = new_position
                self.history.append(f"Moved {direction}")
            else:
                self.history.append(f"Moved {direction} - Hit a wall")

    def act(self):
        if len(self.history) == 0 or self.history[-1].startswith("Moved"):
            if not self.check():
                self.clean()
        else:
            direction = random.choice(["north", "south", "west", "east"])
            self.move(direction)
