from random import randint
import pygame


class Aspirador(pygame.sprite.Sprite):

    def __init__(self) -> None:
        super().__init__()
        
        self.x, self.y = 0, 0
        self.bateria = 10
        self.lixostotais = 0
        
        self.imageIndex = 0
        
        self.spriteSheet = pygame.image.load("Pointer.png")
        width, height = self.spriteSheet.get_size()
                        
        self.images = []
        for i in range(10):
            start_y = i * height // 10  
            end_y = (i + 1) * height // 10
            self.images.append(self.spriteSheet.subsurface((0, start_y, width, end_y - start_y)))

        self.image = self.images[self.imageIndex]
        
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
                print(f" {j} ", end = '')
            print()
            
    def validarDirecao(self, x, y) -> bool:
      return 0 <= self.x + x < self.n and 0 <= self.y + y < self.m

    def validarDirecaoOnScreen(self, x, y) -> bool:
        return 0 < self.rect.x + x < (100*self.n) and 0 < self.rect.y + y < (100*self.m)
  
    def setPos(self, x, y):
        self.x, self.y = x, y
    
    
    def update(self):
        self.imageIndex += 0.5
        self.image = self.images[int(self.imageIndex % 10)]


