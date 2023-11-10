from agent import VacuumAgent


class SpiralVacuum(VacuumAgent):
    """Moves in a spiral anti-clockwise pattern, checking each square it passes by and cleaning it if dirty.

    Turns when hitting a wall or if going back to a previously occupied square"""

    def __init__(self, battery=None, position=[0, 0]):
        super().__init__(battery=battery, position=position)

        self.memory = set()
        self.memory.add(tuple(self.position))
        self.directions = ("south", "east", "north", "west")
        self.next_direction = 0

    def turn(self):
        self.next_direction = (self.next_direction + 1) % 4

    def move(self):
        if self.battery is None or self.battery > 0:
            new_position = None

            times_turned = 0
            while times_turned < 4:
                new_position = self.position.copy()
                direction = self.directions[self.next_direction]

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
                    times_turned += 1
                    self.turn()
                    continue
                elif self.battery:
                    self.battery -= 1

                self.memory.add(memo)
                break

            if times_turned == 4:
                self.history.append("No possible movements")
            elif (
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
