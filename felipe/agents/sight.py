from agent import VacuumAgent


class SuperSightVacuum(VacuumAgent):
    """Finds all dirty squares immediatly for 5% of it's battery, sorting them by distance from the starting square.

    Each time it acts, moves towards the next dirty square. If on a dirty square, cleans it.
    """

    def __init__(self, battery=None):
        super().__init__(battery)
        # Initialize memory to store positions needing cleaning
        self.memory = []

    def check(self):
        if self.battery is None or self.battery >= 5:
            if self.battery:
                self.battery -= 5  # Adjust battery cost for check action
            self.history.append("Checked the entire board for cleanliness")
            self.memory = [
                [i, j]
                for i in range(self.environment.M)
                for j in range(self.environment.N)
                if not self.environment.board[i][j]
            ]

            # Sort positions from closest to furthest
            self.memory.sort(
                key=lambda pos: abs(pos[0] - self.position[0])
                + abs(pos[1] - self.position[1]),
            )

    def act(self):
        if not self.memory:
            self.check()
        elif self.position == self.memory[0]:
            self.memory.pop(0)
            self.clean()
        else:
            # Move towards the next dirty spot
            vertical_distance = self.memory[0][0] - self.position[0]
            horizontal_distance = self.memory[0][1] - self.position[1]

            if vertical_distance != 0:
                direction = "north" if vertical_distance < 0 else "south"
            else:
                direction = "west" if horizontal_distance < 0 else "east"

            self.move(direction)


class OptimizedSuperSightVacuum(VacuumAgent):
    """Finds all dirty squares immediatly for 5% of it's battery.

    Each time it acts:
    - If on a dirty square, cleans it.
    - If it doesn't know the nearest dirty square, sorts all known dirty squares by distance.
    - Otherwise, moves towards the nearest dirty square.
    """

    def __init__(self, battery=None):
        super().__init__(battery)
        # Initialize memory to store positions needing cleaning
        self.memory = set()
        # Nearest dirty square
        self.target = None

    def check(self):
        if self.battery is None or self.battery >= 5:
            if self.battery:
                self.battery = round(
                    0.95 * self.battery
                )  # Adjust battery cost for check action
            self.history.append("Checked the entire board for cleanliness")
            self.memory = {
                (i, j)
                for i in range(self.environment.M)
                for j in range(self.environment.N)
                if not self.environment.board[i][j]
            }

    def act(self):
        if not self.memory:
            self.check()
        else:
            if (current_position := tuple(self.position)) in self.memory:
                self.memory.remove(current_position)
                self.target = None
                self.clean()
            elif self.target is None:
                dirty_positions = sorted(
                    self.memory,
                    key=lambda pos: abs(pos[0] - self.position[0])
                    + abs(pos[1] - self.position[1]),
                )
                self.target = dirty_positions[0]
            else:
                # Move towards the nearest dirty spot
                vertical_distance = self.target[0] - self.position[0]
                horizontal_distance = self.target[1] - self.position[1]

                if vertical_distance != 0:
                    direction = "north" if vertical_distance < 0 else "south"
                else:
                    direction = "west" if horizontal_distance < 0 else "east"

                self.move(direction)
