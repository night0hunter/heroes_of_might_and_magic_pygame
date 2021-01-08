import pygame
import os
import sys
from board import Board, load_image
import sqlite3
from per_menu import InputBox


input_boxes = []
if __name__ == "__main__":
    font = pygame.font.Font(None, 24)
    size = 1500, 700
    for i in range(10):
        if i < 2:
            if i < 9:
                input_boxes.append(InputBox(15, 80, 50, 30))
                input_boxes.append(InputBox(15, 70 * 2, 50, 30))

            input_boxes.append(InputBox(1350, 80, 50, 30))
            input_boxes.append(InputBox(1350, 70 * 2, 50, 30))
        else:
            if i < 9:
                input_boxes.append(InputBox(15 , 65 * (i + 1), 50, 30))

            input_boxes.append(InputBox(1350 , 65 * (i + 1), 50, 30))

    screen = pygame.display.set_mode(size)    
    screen2 = pygame.Surface(screen.get_size())
    screen.fill((0, 0, 0))
    a = Board(size[0], size[1], 8, 10)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   
                running = False
            for box in input_boxes:
                box.handle_event(event)

        screen.fill((0, 0, 0))
        for box in input_boxes:
            box.draw(screen)
        a.draw_sprite()
        a.drawForChoice("white")
       
        pygame.display.flip()
    pygame.quit()


