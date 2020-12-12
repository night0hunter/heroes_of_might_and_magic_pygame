import pygame
import sqlite3
import math


con = sqlite3.connect("heroes_of_might_and_magic_pygame\\units.db")
cur = con.cursor()
pygame.init()

class Board:
    def __init__(self, width, height, num):
        self.height = height
        self.width = width
        self.size = width, height
        self.num = num
        #список клеток с персонажами
        self.list_per = []
        for i in range(8):
            b = []
            for j in range(8):
                b.append(0)
            self.list_per.append(b)
        # значения по умолчанию
        self.size_k = 50
        self.top = 50
        self.left = 50

    # функция настройки
    def setting(self, left, top, size):
        self.left = left
        self.top = top
        self.size_k = size

    # функция рисования поля
    def draw(self, color):
        for i in range(self.num):
            for j in range(self.num):
                pygame.draw.rect(screen, pygame.Color(str(color)),
                                (self.left + self.size_k * j, self.top + self.size_k * i,
                                 self.size_k, self.size_k), 1)

    # функия получения координат клетки по типу [x, y] пример (0, 3)
    def get_coords(self, coord_x, coord_y):
        x, y = coord_x, coord_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return [x, y]

    def move_option(self, coord_x, coord_y, person):
        result = cur.execute(f"""SELECT speed FROM unit_stats WHERE name == '{person}'""").fetchone()
        print(result)
        result = int(result[0]) + 1
        x, y = coord_x, coord_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        self.list_move = []
        #обновление при каждом вызове, создание массива с координатами клеткок
        for i in range(self.num):
            b = []
            for j in range(self.num):
                b.append([i, j])
            self.list_move.append(b)
        #перестройка массива с координат на True or False, где True = может дойти, а False = не может
        for i in range(self.num):
            for j in range(self.num):
                self.list_move[i][j] = True
                if x >= j:
                    if y >= i and result <= x - j + y - i:
                        self.list_move[i][j] = False
                    elif y < i and result <= x - j + i - y:
                        self.list_move[i][j] = False
                else:
                    if y >= i and result <= j - x + y - i:
                        self.list_move[i][j] = False
                    elif y < i and result <= j - x + i - y:
                        self.list_move[i][j] = False
        return self.list_move

    def in_board(self, coord_x, coord_y):
        if self.left <= coord_x <= self.left + self.size_k * self.num:
            if self.top <= coord_y <= self.top + self.size_k * self.num:
                return True
        return False
    
    def p_list_per(self):
        for i in self.list_per:
            print(i)
        print('')
            
size = 800, 600
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
a = Board(size[0], size[1], 8)
a.setting(10, 10, 50)
a.draw("white")
person = "Крестьянин"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            a.p_list_per()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if a.in_board(event.pos[0], event.pos[1]):
                #get_click(event.pos[0], event.pos[1])
                for i in a.move_option(event.pos[0], event.pos[1], person):
                    print(i)
                print(' ')


    pygame.display.flip()

pygame.quit()
con.close()