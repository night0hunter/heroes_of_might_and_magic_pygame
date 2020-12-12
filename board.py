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
        self.list_move = []
        for i in range(self.num):
            b = []
            c = []
            for j in range(self.num):
                b.append(0)
                c.append(False)
            self.list_per.append(b)
            self.list_move.append(c)
        # значения по умолчанию
        self.size_k = 50
        self.top = 50
        self.left = 50
        self.list_move = []
        self.coord_x = 0
        self.coord_y = 0

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

    def get_click(self, coord_x, coord_y):
        pass

    def draw_move_option(self):
        color = pygame.Color(50, 150, 50)
        if self.list_move != []:
            for i in range(self.num ):
                for j in range(self.num):
                    if self.list_move[i][j] is True and self.list_per[i][j] == 0:
                        pygame.draw.rect(screen2, color, (self.left + self.size_k * j + 1,
                        self.top + self.size_k * i + 1,
                        self.size_k - 2, self.size_k - 2))

    def move_option(self, coord_x, coord_y, person):
        self.coord_x = coord_x
        self.coord_y = coord_y
        result = cur.execute(f"""SELECT speed FROM unit_stats WHERE name == '{person}'""").fetchone()
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
screen2 = pygame.Surface(screen.get_size())
screen.fill((0, 0, 0))
a = Board(size[0], size[1], 8)
a.setting(10, 10, 70)
clock = pygame.time.Clock()
FPS = 60
person = "Крестьянин"
running = True
draw = False
while running:
    screen.blit(screen2, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            a.p_list_per()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if a.in_board(event.pos[0], event.pos[1]):
                a.get_click(event.pos[0], event.pos[1])
                a.move_option(event.pos[0], event.pos[1], person)
                screen2.fill((0, 0, 0))
                a.draw_move_option()
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    screen.blit(screen2, (0, 0))
    a.draw("white")
    pygame.display.flip()

pygame.quit()
con.close()