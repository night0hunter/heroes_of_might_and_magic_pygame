import pygame
import os
import sys
from board import Board, load_image
import sqlite3
from per_menu import InputBox
from menu import Menu



con = sqlite3.connect("C:\Github\heroes_of_might_and_magic_pygame\\units.db")
cur = con.cursor()
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)  
running = True
font = pygame.font.Font(None, 60)
a = Menu(size[0], size[1])
clock = pygame.time.Clock()
FPS = 300
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False 
    a.draw(screen, font)
    clock.tick(FPS)
    pygame.display.flip()


input_boxes = []
data = {
       "Крестьянин": 1,
       "Ополченец с щитом": 1,
       "Ополченец с луком": 1,
       "Наемник с копьем": 1,
       "Наемник с щитом": 1,
       "Паладин": 1,
       "Рыцарь": 1,
       "Маг": 1,
       "Ангел": 1,
       "Скелет": 1,
       "Зомби": 1,
       "Адский пес": 1,
       "Привидение": 1,
       "Паук": 1,
       "Вампир": 1,
       "Некромант": 1,
       "Демон": 1,
       "Костяной дракон": 1,
       "Лич": 1
   }


font = pygame.font.Font(None, 24)
size = 1400, 700
size1 = 300, 50

for i in range(9):
    input_boxes.append(InputBox(15, 65 * (i + 1), 50, 30))
for i in range(10):
    input_boxes.append(InputBox(1350, 65 * (i + 1), 50, 30))


screen = pygame.display.set_mode(size)
screen2 = pygame.Surface(screen.get_size())
screen.fill((0, 0, 0))
b = Board(size[0], size[1], 8, 10)
running = True
target = None
noTarget = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            running = False 
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            screen2.fill((0, 0, 0))
            if not(b.in_board2(event.pos[0], event.pos[1])):
                target = b.draw_target_picture(screen2, event.pos[0], event.pos[1])
                if target != None and target not in noTarget:
                    b.draw_move_option2(screen2, target)
            if b.in_board2(event.pos[0], event.pos[1]) and target != None and target not in noTarget:
                if b.in_list_move2(event.pos[0], event.pos[1]):
                    b.make_pers(event.pos[0], event.pos[1], target)
                    noTarget.append(target)
                    target = None
                
        for box in input_boxes:
            box.handle_event(event)

    screen.fill((0, 0, 0))
    screen.blit(screen2, (0, 0))
    for box in input_boxes:
        box.draw(screen)

    b.draw_sprite(screen)
    b.draw_person2(screen2)
    b.drawForChoice("white", screen)
    pygame.display.flip()
j = 0
for i in data.keys():
    hp = cur.execute(f"""SELECT health FROM unit_stats WHERE name = '{i}'""").fetchone()
    hp = hp[0]
    a = input_boxes[j].text
    if a == "":
        a = 1
    data[i] = [a, int(a) * int(hp)]
    j += 1


abc = b.rtn_list_per()

size = 1100, 700
size1 = 300, 50
screen = pygame.display.set_mode(size)    
screen2 = pygame.Surface(screen.get_size())
screen3 = pygame.Surface(size1)
screen.fill((0, 0, 0))
screen3.fill((255, 0, 0))
a = Board(size[0], size[1], 8, 10)
a.setting(10, 10, 70)

all_sprites = pygame.sprite.Group()
sprite = pygame.sprite.Sprite(all_sprites)
sprite.image = load_image("arrow.png")
sprite.rect = sprite.image.get_rect()

clock = pygame.time.Clock()
FPS = 1440
running = True
Move = False
Info = False
Attack = False
Only_attack = False
pygame.mouse.set_visible(False)
draw = False
a.input_list_per(abc)
hod = a.make_hod(data)
target = hod[0]
font = pygame.font.Font(None, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            screen2.fill((0, 0, 0))
            if a.in_board(event.pos[0], event.pos[1]):
                if not Move and a.in_list_per(event.pos[0], event.pos[1]) != 0:
                    target = a.pers(event.pos[0], event.pos[1])
                    a.move_option(event.pos[0], event.pos[1])
                    a.attack_option(event.pos[0], event.pos[1])
                    Move = True
                    Info = True
                    arr = a.get_coords(event.pos[0], event.pos[1])
                    a.draw_move_option(screen2)
                    a.draw_attack(screen2, event.pos[0], event.pos[1], target)
                elif target == hod[0] and a.in_list_per(event.pos[0], event.pos[1]) != 0 and a.in_list_attack(event.pos[0], event.pos[1]):
                    [data, hod] = a.make_attack(target, data, event.pos[0], event.pos[1], hod)
                    Attack = True
                    del hod[0]
                    if len(hod) == 0:
                        hod = a.make_hod(data)
                    Move = False
                    Info = False
                elif Move and a.in_list_move(event.pos[0], event.pos[1]) and target == hod[0]:
                    if arr != a.get_coords(event.pos[0], event.pos[1]):
                        if a.in_list_per(event.pos[0], event.pos[1]) == 0:
                            a.make_move(arr, event.pos[0], event.pos[1])
                            del hod[0]
                            if len(hod) == 0:
                                hod = a.make_hod(data)
                    Move = False
                    Info = False
                else:
                    Move = False
                    Info = False
            else:
                Move = False
                Info = False
                if 50 <= event.pos[0] <= 330 and 590 <= event.pos[1] <= 640:
                    del hod[0]
                    if len(hod) == 0:
                        hod = a.make_hod(data)
        if event.type == pygame.MOUSEMOTION:
            sprite.rect.x = event.pos[0]
            sprite.rect.y = event.pos[1]
            if pygame.mouse.get_focused():
                draw = True
            else:
                draw = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            screen2.fill((0, 0, 0))
            Move = False
            Info = False
        a.draw_person(screen2)
        screen.blit(screen2, (0, 0))
        a.draw("white", screen)
        text = font.render(f"{hod[0]}", True, (100, 255, 100))
        screen.blit(text, (350, 600))
        if Info:
            font1 = pygame.font.Font(None, 30)
            y1 = 50
            for i in a.text_info(target, data):
                text = font1.render(i, True, (100, 255, 100))
                screen.blit(text, (800, y1))
                y1 += 30
        #if Attack is True:
        #    Attack = a.animation_attack()
        if True:
            a.draw_button(screen, 50, 600)
        if draw:
            all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

pygame.quit()