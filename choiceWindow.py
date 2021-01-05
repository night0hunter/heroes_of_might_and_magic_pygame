import pygame
import os
import sys
from board import Board, load_image
import sqlite3


if __name__ == "__main__":
    size = 1000, 700
    screen = pygame.display.set_mode(size)    
    screen2 = pygame.Surface(screen.get_size())
    screen.fill((0, 0, 0))
    a = Board(size[0], size[1], 8, 10)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                running = False
        a.draw_sprite()
        a.drawForChoice("white")
        pygame.display.flip()
    pygame.quit()


