import pygame
import os
import sys
from board import Board, load_image
import sqlite3
from per_menu import InputBox


input_boxes = []
data = {
       "Крестьянин": None,
       "Ополченец с щитом": None,
       "Ополченец с луком": None,
       "Наемник с копьем": None,
       "Наемник с щитом": None,
       "Паладин": None,
       "Рыцарь": None,
       "Маг": None,
       "Ангел": None,
       "Скелет": None,
       "Зомби": None,
       "Адский пес": None,
       "Привидение": None,
       "Паук": None,
       "Вампир": None,
       "Некромант": None,
       "Демон": None,
       "Костяной дракон": None,
       "Лич": None
   }

if __name__ == "__main__":
    font = pygame.font.Font(None, 24)
    size = 1500, 700
   
    for i in range(9):
        input_boxes.append(InputBox(15, 65 * (i + 1), 50, 30))
    for i in range(10):
        input_boxes.append(InputBox(1350, 65 * (i + 1), 50, 30))


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
    j = 0   
    for i in data.keys():
        data[i] = input_boxes[j].text
        j += 1
    print(data)
    pygame.quit()


