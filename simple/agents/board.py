import random


class Board:
    def __init__(self, M, N) -> None:
        self.M = M
        self.N = N
        self.board = [[True] * N for _ in range(M)]  # Initialize all positions as clean

    def dirt(self, dirt):
        self.board = [[True] * self.N for _ in range(self.M)]
        # Randomly set specified number of dirty spaces
        dirty_positions = set()
        while len(dirty_positions) < dirt:
            i, j = random.randint(0, self.M - 1), random.randint(0, self.N - 1)
            dirty_positions.add((i, j))
            self.board[i][j] = False
