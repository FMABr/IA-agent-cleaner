import pygame
import random
from Garbage import Garbage
from random import randint
from Aspirador import Aspirador

# Inicialização do Pygame
pygame.init()


larguraMundo, alturaMundo = 10, 10
# Defina a tela e o personagem (player)
screen = pygame.display.set_mode((larguraMundo*100, alturaMundo*100))


player = Aspirador()
player.setPos(0, 0)


 #Variáveis para o tamanho do mundo

mundo = player.criarMundo(larguraMundo, alturaMundo)

player_sprite = pygame.sprite.Group()
player_sprite.add(player)

all_sprites = pygame.sprite.Group()



for i in range(len(mundo)):
    for j in range(len(mundo)):
         if mundo[i][j] == 1:
            sprite = Garbage(100*i, 100*j)    
            all_sprites.add(sprite)



clock = pygame.time.Clock()
FPS = 60  # Defina o FPS desejado


# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False




    #player.moveOnScreen()
    #Função para mover o aspirador
   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 1
    if keys[pygame.K_RIGHT]:
        player.rect.x += 1
    if keys[pygame.K_UP]:
        player.rect.y -= 1
    if keys[pygame.K_DOWN]:
        player.rect.y += 1
        
        
        
        
        

    collided_sprites = pygame.sprite.spritecollide(player, all_sprites, True)

    for sprite in collided_sprites:
        all_sprites.remove(sprite)

    screen.fill((0, 0, 0))
    
    player.update()

    all_sprites.draw(screen)
    player_sprite.draw(screen)
    
    
    clock.tick(FPS)


    pygame.display.flip()

pygame.quit()
