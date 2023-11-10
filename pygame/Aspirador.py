from random import randint
import pygame

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


class Aspirador(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.x, self.y = 0, 0
        self.bateria = 10
        self.lixostotais = 0

        self.imageIndex = 0

        self.spriteSheet = pygame.image.load("miguel/Pointer.png")
        width, height = self.spriteSheet.get_size()

        self.images = []
        for i in range(10):
            start_y = i * height // 10
            end_y = (i + 1) * height // 10
            self.images.append(
                self.spriteSheet.subsurface((0, start_y, width, end_y - start_y))
            )

        self.image = self.images[self.imageIndex]

        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y

    def limpar(self, mundo) -> None:
        if mundo[self.x][self.y] == 1:
            mundo[self.x][self.y] = 0
        self.bateria -= 0.1

    def mover(self) -> None:
        dir = randint(-1, 1)

        if randint(0, 1) == 1:
            if self.validarDirecao(dir, 0):
                self.x += dir
        else:
            if self.validarDirecao(0, dir):
                self.y += dir
        self.bateria -= 0.05

    def moveOnScreen(self) -> None:
        dir = randint(1, 4)

        if dir == 1:
            if self.validarDirecao(self.rect.x - 100, self.rect.y):
                self.rect.x -= 100
        elif dir == 2:
            if self.validarDirecao(self.rect.x + 100, self.rect.y):
                self.rect.x += 100
        elif dir == 3:
            if self.validarDirecao(self.rect.x, self.rect.y - 100):
                self.rect.y -= 100
        else:
            if self.validarDirecao(self.rect.x, self.rect.y + 100):
                self.rect.y += 100

    def criarMundo(self, m, n) -> list:
        self.m = m
        self.n = n

        mundo = []
        for i in range(m):
            aux = []
            for i in range(n):
                num = randint(0, 1)
                self.lixostotais += 1 if num == 1 else 0
                aux.append(num)
            mundo.append(aux)
        return mundo

    def showMundo(self, mundo) -> None:
        for i in mundo:
            for j in i:
                print(f" {j} ", end="")
            print()

    def validarDirecao(self, x, y) -> bool:
        return 0 <= self.x + x < self.n and 0 <= self.y + y < self.m

    def validarDirecaoOnScreen(self, x, y) -> bool:
        return 0 < self.rect.x + x < (100 * self.n) and 0 < self.rect.y + y < (
            100 * self.m
        )

    def setPos(self, x, y):
        self.x, self.y = x, y

    def update(self):
        self.imageIndex += 0.5
        self.image = self.images[int(self.imageIndex % 10)]
