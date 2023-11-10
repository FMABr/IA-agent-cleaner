import pygame
import random
from Garbage import Garbage


# Inicialização do Pygame
pygame.init()

# Defina a tela e o personagem (player)
screen = pygame.display.set_mode((800, 600))
player = pygame.sprite.Sprite()
player.image = pygame.Surface((50, 50))
player.image.fill((255, 0, 0))
player.rect = player.image.get_rect()
player.rect.center = (400, 300)

# Crie um grupo de sprites
all_sprites = pygame.sprite.Group()

# Adicione algumas sprites aleatórias ao grupo
for _ in range(10):
    sprite = Garbage(random.randint(0, 800), random.randint(0, 600))
    
    all_sprites.add(sprite)

# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualize a posição do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= 1
    if keys[pygame.K_RIGHT]:
        player.rect.x += 1
    if keys[pygame.K_UP]:
        player.rect.y -= 1
    if keys[pygame.K_DOWN]:
        player.rect.y += 1

    # Verifique colisões entre o jogador e as sprites
    collided_sprites = pygame.sprite.spritecollide(player, all_sprites, True)

    # Remova as sprites que colidiram do grupo
    for sprite in collided_sprites:
        all_sprites.remove(sprite)

    # Limpe a tela
    screen.fill((0, 0, 0))

    # Desenhe todos os sprites restantes
    all_sprites.draw(screen)
    pygame.draw.rect(screen, (255, 0, 0), player.rect)
    


    pygame.display.flip()

pygame.quit()
