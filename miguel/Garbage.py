import pygame
from random import randint

class Garbage(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        
        self.spriteSheet = pygame.image.load("littered_dungeon.png")
        images = []
        
        width, height = self.spriteSheet.get_size()
        
        
        for i in range(4):
            left = i * (width / 4)
            top = 2 * (height / 3)
            right = (i + 1) * (width / 4)
            bottom = height
            images.append(self.spriteSheet.subsurface((left, top, right - left, bottom - top)))

        images.append(self.spriteSheet.subsurface((width/2, height/3, width/4, height/3))) 
        images.append(self.spriteSheet.subsurface((3*width/4, height/3, width/4, height/3)))

        self.image = images[randint(0, 5)]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        
        
        
        
