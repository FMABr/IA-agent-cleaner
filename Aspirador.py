from random import randint
import pygame


class Aspirador(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        
        self.x, self.y = 0, 0
        self.bateria = 10
        self.lixostotais = 0
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y


    def limpar(self, mundo) -> None:
        if mundo[self.x][self.y] == 1:
            mundo[self.x][self.y] = 0
        self.bateria -= 0.1

    def mover(self) -> None:
      dir = randint(-1,1)

      if randint(0,1) == 1:
        if self.validarDirecao(dir, 0):
          self.x += dir
      else:
        if self.validarDirecao(0, dir):
          self.y += dir
      self.bateria -= 0.05

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
                print(f" {j} ", end = '')
            print()
            
    def validarDirecao(self, x, y) -> bool:
      return 0 <= self.x + x < self.n and 0 <= self.y + y < self.m

    def update(self) -> None:
        pass

