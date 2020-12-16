import os
import sys
import pygame
import random

# Изображение не получится загрузить
# без предварительной инициализации pygame
pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = load_image("arrow.png")
sprite.rect = sprite.image.get_rect()


clock = pygame.time.Clock()
fps = 1440
running = True
pygame.mouse.set_visible(False)
draw = True
while running:
    screen.fill(pygame.Color("black"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            sprite.rect.x = event.pos[0]
            sprite.rect.y = event.pos[1]
            if pygame.mouse.get_focused():
                draw = True
            else:
                draw = False
    if draw:
        all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

