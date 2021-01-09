import pygame
import os
import sys
from board import Board, load_image
import sqlite3
from per_menu import InputBox


input_boxes = []
data = {
       "Крестьянин": 0,
       "Ополченец с щитом": 0,
       "Ополченец с луком": 0,
       "Наемник с копьем": 0,
       "Наемник с щитом": 0,
       "Паладин": 0,
       "Рыцарь": 0,
       "Маг": 0,
       "Ангел": 0,
       "Скелет": 0,
       "Зомби": 0,
       "Адский пес": 0,
       "Привидение": 0,
       "Паук": 0,
       "Вампир": 0,
       "Некромант": 0,
       "Демон": 0,
       "Костяной дракон": 0,
       "Лич": 0
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


