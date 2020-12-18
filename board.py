import pygame
import sqlite3
import os
import sys


con = sqlite3.connect("C:\Github\heroes_of_might_and_magic_pygame\\units.db")
cur = con.cursor()
pygame.init()
pygame.display.set_caption("Система боя от Героев Меча и Магии")

class Board:
    # вводятся значения экрана и значения по умолчанию
    def __init__(self, width, height, num1, num2):
        self.height = height
        self.width = width
        self.size = width, height
        self.num1 = num1
        self.num2 = num2
        #список клеток с персонажами
        self.list_per = []
        self.list_move = []
        for i in range(self.num1):
            b = []
            c = []
            for j in range(self.num2):
                b.append(0)
                c.append(False)
            self.list_per.append(b)
            self.list_move.append(c)
        # значения по умолчанию
        self.size_k = 50
        self.top = 50
        self.left = 50
        self.list_move = []

    # функция настройки
    def setting(self, left, top, size):
        self.left = left
        self.top = top
        self.size_k = size

    # функция рисования поля
    def draw(self, color):
        for i in range(self.num1):
            for j in range(self.num2):
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

    # функция прорисовки возможности хода
    def draw_move_option(self):
        color = pygame.Color(50, 150, 50)
        if self.list_move != [] and self.list_per != []:
            for i in range(self.num1):
                for j in range(self.num2):
                    if self.list_move[i][j] is True and self.list_per[i][j] == 0:
                        pygame.draw.rect(screen2, color, (self.left + self.size_k * j + 1,
                        self.top + self.size_k * i + 1,
                        self.size_k - 2, self.size_k - 2))

    # функция генерирующая список возможностей хода
    def move_option(self, coord_x, coord_y, person):
        result = cur.execute(f"""SELECT speed FROM unit_stats WHERE name == '{person}'""").fetchone()
        result = int(result[0]) + 1
        x, y = coord_x, coord_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        self.list_move = []
        #обновление при каждом вызове, создание массива с координатами клеток
        for i in range(self.num1):
            b = []
            for j in range(self.num2):
                b.append([i, j])
            self.list_move.append(b)
        #перестройка массива с координат на True or False, где True = может дойти, а False = не может
        for i in range(self.num1):
            for j in range(self.num2):
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

    # функция проверки на место нажатия
    def in_board(self, coord_x, coord_y):
        if self.left <= coord_x <= self.left + self.size_k * self.num2:
            if self.top <= coord_y <= self.top + self.size_k * self.num1:
                return True
        return False
      
    #связующая функция изменения списка местоположения персонажей
    def input_list_per(self, list):
        self.list_per = list
    
    def in_list_per(self, pos_x, pos_y):
        x, y = pos_x, pos_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        if self.list_per[y][x] == 1:
            return True
        return False
    
    def in_list_move(self, pos_x, pos_y):
        x, y = pos_x, pos_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return self.list_move[y][x]
    
    def make_move(self, arr, pos_x, pos_y):
        a = self.list_per[arr[1]][arr[0]]
        print(arr[0], arr[1])
        x, y = pos_x, pos_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        print(y, x)
        self.list_per[arr[1]][arr[0]] = 0
        self.list_per[y][x] = a


abc = [[1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1],
       [1, 0, 0, 0, 0, 0, 0, 1]]

 
size = 800, 600
screen = pygame.display.set_mode(size)    
screen2 = pygame.Surface(screen.get_size())
screen.fill((0, 0, 0))
a = Board(size[0], size[1], 8, 8)
a.setting(10, 10, 70)

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
FPS = 144
person = "Костяной дракон"
running = True
Move = False
pygame.mouse.set_visible(False)
draw = False
a.input_list_per(abc)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pygame.mouse.set_visible(True)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            screen2.fill((0, 0, 0))
            if a.in_board(event.pos[0], event.pos[1]):
                if not Move and a.in_list_per(event.pos[0], event.pos[1]):
                    a.move_option(event.pos[0], event.pos[1], person)
                    a.draw_move_option()
                    Move = True
                    arr = a.get_coords(event.pos[0], event.pos[1])
                elif Move and a.in_list_move(event.pos[0], event.pos[1]):
                    if arr != a.get_coords(event.pos[0], event.pos[1]):
                        if not a.in_list_per(event.pos[0], event.pos[1]):
                            a.make_move(arr, event.pos[0], event.pos[1])
                    Move = False
                else:
                    Move = False
            else:
                Move = False
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
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        screen.blit(screen2, (0, 0))
        a.draw("white")
        if draw:
            all_sprites.draw(screen)
        pygame.display.flip()

pygame.quit()
con.close()