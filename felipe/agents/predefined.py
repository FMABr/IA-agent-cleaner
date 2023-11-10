from agent import VacuumAgent


class SpiralVacuum(VacuumAgent):
    """Moves in a spiral anti-clockwise pattern, checking each square it passes by and cleaning it if dirty.

    Turns when hitting a wall or if going back to a previously occupied square"""

    def __init__(self, battery=None):
        super().__init__(battery)

        self.memory = set()
        self.memory.add(tuple(self.position))
        self.directions = ("south", "east", "north", "west")
        self.next_direction = 0

    def turn(self):
        self.next_direction = (self.next_direction + 1) % 4

    def move(self):
        if self.battery is None or self.battery > 0:
            direction = self.directions[self.next_direction]
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
                self.turn()
                return
            elif self.battery:
                self.battery -= 1

            self.memory.add(memo)

            if (
                0 <= new_position[0] < self.environment.M
                and 0 <= new_position[1] < self.environment.N
            ):
                self.position = new_position
                self.history.append(f"Moved {direction}")
            else:
                self.turn()
                self.history.append(f"Moved {direction} - Hit a wall")

    def act(self):
        if len(self.history) == 0 or self.history[-1].startswith("Moved"):
            if not self.check():
                self.clean()
        else:
            self.move()
