from abc import ABC, abstractmethod


class VacuumAgent(ABC):
    def __init__(self, battery=None, position=[0, 0]):
        self.position = position
        self.battery = battery
        self.history = []
        self.environment = None

    def move(self, direction):
        if self.battery is None or self.battery > 0:
            if self.battery:
                self.battery -= 1

            new_position = self.position.copy()

            if direction == "north":
                new_position[0] -= 1
            elif direction == "south":
                new_position[0] += 1
            elif direction == "west":
                new_position[1] -= 1
            elif direction == "east":
                new_position[1] += 1

            if (
                0 <= new_position[0] < self.environment.M
                and 0 <= new_position[1] < self.environment.N
            ):
                self.position = new_position
                self.history.append(f"Moved {direction}")
            else:
                self.history.append(f"Moved {direction} - Hit a wall")

    def check(self):
        self.history.append(
            f"Checked position ({self.position[0]}, {self.position[1]}) for cleanliness"
        )

        return self.environment.board[self.position[0]][self.position[1]]

    def clean(self):
        if self.battery is None or self.battery > 0:
            if self.battery:
                self.battery -= 1

            if not self.environment.board[self.position[0]][self.position[1]]:
                self.history.append(
                    f"Cleaned position ({self.position[0]}, {self.position[1]})"
                )
                self.environment.board[self.position[0]][self.position[1]] = True

    def run(self, env, log=False):
        self.environment = env
        while self.battery is None or self.battery > 0:
            if all(all(cell for cell in row) for row in self.environment.board):
                break

            self.act()

            if self.history[-1] == "No possible movements":
                break

            if log:
                print(self.history[-1])

    @abstractmethod
    def act(self):
        pass
