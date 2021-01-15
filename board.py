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
        self.list_attack = []
        for i in range(self.num1):
            b = []
            c = []
            for j in range(self.num2):
                b.append(0)
                c.append(False)
            self.list_per.append(b)
            self.list_move.append(c)
            self.list_attack.append(c)
        # значения по умолчанию
        self.size_k = 50
        self.size_k1 = 65
        self.top = 60
        self.left = 50
        self.coords_picture = []

    # функция настройки
    def setting(self, left, top, size):
        self.left = left
        self.top = top
        self.size_k = size
    
    def rtn_list_per(self):
        return self.list_per

    # функция рисования поля
    def draw(self, color, screen):
        for i in range(self.num1):
            for j in range(self.num2):
                pygame.draw.rect(screen, pygame.Color(str(color)),
                                (self.left + self.size_k * j, self.top + self.size_k * i,
                                 self.size_k, self.size_k), 1)

    def drawForChoice(self, color, screen):
        for i in range(self.num1):
            for j in range(self.num2):
                pygame.draw.rect(screen, pygame.Color(str(color)),
                                (self.left + 350 + self.size_k1 * j, self.top + self.size_k1 * i,
                                 self.size_k1, self.size_k1), 1)

    # функия получения координат клетки по типу [x, y] пример (0, 3)
    def get_coords(self, coord_x, coord_y):
        x, y = coord_x, coord_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return [x, y]
                                                    
    # функция прорисовки возможности хода
    def draw_move_option(self, screen2):
        color = pygame.Color(50, 150, 50)
        if self.list_move != [] and self.list_per != []:
            for i in range(self.num1):
                for j in range(self.num2):
                    if self.list_move[i][j] is True and self.list_per[i][j] == 0:
                        pygame.draw.rect(screen2, color, (self.left + self.size_k * j + 1,
                        self.top + self.size_k * i + 1,
                        self.size_k - 2, self.size_k - 2))

    # функция генерирующая список возможностей хода
    def move_option(self, coord_x, coord_y):
        x, y = coord_x, coord_y
        x -= self.left
        y -= self.top
        x //= self.size_k
        y //= self.size_k
        result = cur.execute(f"""SELECT speed FROM unit_stats WHERE name == '{self.list_per[y][x]}'""").fetchone()
        result = int(result[0]) + 1
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
    
    def in_board2(self, x, y):
        if self.left + 350 <= x <= self.left + 350 + self.size_k1 * self.num2:
            if self.top <= y <= self.top + self.size_k1 * self.num1:
                return True
        return False
      
    #связующая функция изменения списка местоположения персонажей
    def input_list_per(self, list):
        self.list_per = list
    
    #функция проверки если на клетке никого нет вернет False если кто-то есть вернет True 
    def in_list_per(self, pos_x, pos_y):
        x, y = pos_x, pos_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return self.list_per[y][x]
    
    #функция проверки если на клетке никого нет вернет False если кто-то есть вернет True 
    def in_list_move(self, pos_x, pos_y):
        x, y = pos_x, pos_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return self.list_move[y][x]
    
    def in_list_move2(self, x, y):
        x -= (self.left + 350)
        y -= self.top
        x = x // self.size_k1
        y = y // self.size_k1
        return self.list_move[y][x]

    #функция хода  
    def make_move(self, arr, pos_x, pos_y):
        a = self.list_per[arr[1]][arr[0]]
        x, y = pos_x, pos_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        self.list_per[arr[1]][arr[0]] = 0
        self.list_per[y][x] = a

    def draw_person(self, screen2):
        all_sprites2 = pygame.sprite.Group()
        for y in range(self.num1):
            for x in range(self.num2):
                if self.list_per[y][x] != 0:
                    sprite = pygame.sprite.Sprite(all_sprites2)
                    if self.list_per[y][x] == "Костяной дракон":
                        sprite.image = load_image(f"{self.list_per[y][x]}.png")
                    else:    
                        sprite.image = load_image(f"{self.list_per[y][x]}.png", colorkey=-1)
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = self.left + self.size_k * x + 1
                    sprite.rect.y = self.top + self.size_k * y + 1
        all_sprites2.draw(screen2)
    
    def draw_person2(self, screen):
        all_sprites2 = pygame.sprite.Group()
        for y in range(self.num1):
            for x in range(self.num2):
                if self.list_per[y][x] != 0:
                    sprite = pygame.sprite.Sprite(all_sprites2)
                    if self.list_per[y][x] == "Костяной дракон":
                        sprite.image = load_image(f"{self.list_per[y][x]}.png")
                    else:    
                        sprite.image = load_image(f"{self.list_per[y][x]}.png", colorkey=-1)
                    sprite.rect = sprite.image.get_rect()
                    
                    sprite.rect.x = self.left + 350 + self.size_k1 * x + 1
                    sprite.rect.y = self.top - 10 + self.size_k1 * y + 1
                    if self.list_per[y][x] == "Костяной дракон" or self.list_per[y][x] == "Паук":
                        sprite.rect.y = self.top + self.size_k1 * y + 1
        all_sprites2.draw(screen)

    def draw_sprite(self, screen):
        self.coords_picture = []
        result = cur.execute("""SELECT name FROM unit_stats WHERE fraction == 1""").fetchall()
        result2 = cur.execute("""SELECT name FROM unit_stats WHERE fraction == 0""").fetchall()
        all_sprites3 = pygame.sprite.Group()
        all_sprites4 = pygame.sprite.Group()
        color = pygame.Color("white")
        font = pygame.font.Font(None, 24)

        for i in range(len(result)):
            sprite = pygame.sprite.Sprite(all_sprites3)
            sprite.image = load_image(f"{result[i][0]}.png", colorkey=-1)

            text = font.render(result[i][0], True, color)
            
            if result[i][0] == "Крестьянин":
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = self.left + 50
                sprite.rect.y = (self.top - 10) * (i + 1)
                self.coords_picture.append([self.left + 50, (self.top - 10) * (i + 1), result[i][0]])
                place = text.get_rect(center=(self.left + 200, (self.top - 10) * (i + 2)))
            else:
                sprite.rect = sprite.image.get_rect()
                sprite.rect.x = self.left + 50
                sprite.rect.y = self.top * (i + 1)
                self.coords_picture.append([self.left + 50, self.top * (i + 1), result[i][0]])
                place = text.get_rect(center=(self.left + 200, (self.top - 2) * (i + 2)))
            screen.blit(text, place)
        all_sprites3.draw(screen)

        for i in range(len(result2)):
            sprite1 = pygame.sprite.Sprite(all_sprites4)
            if result2[i][0] == "Костяной дракон":
                sprite1.image = load_image(f"{result2[i][0]}.png")
            else:
                sprite1.image = load_image(f"{result2[i][0]}.png", colorkey=-1)
            sprite1.rect = sprite1.image.get_rect()
            sprite1.rect.x = 1280 - self.left
            sprite1.rect.y = (self.top + 2)* (i + 1)
            self.coords_picture.append([1280 - self.left, (self.top + 2)* (i + 1), result2[i][0]])

            text = font.render(result2[i][0], True, color)
            place = text.get_rect(center=(1200 - self.left, self.top * (i + 2)))
            screen.blit(text, place)
        all_sprites4.draw(screen)
     
    def draw_target_picture(self, screen4, x, y):
        color = pygame.Color(50, 150, 50)
        for i in self.coords_picture:
            if i[0] <= x <= i[0] + 70 and i[1] <= y <= i[1] + 70:
                pygame.draw.rect(screen4, color, (i[0], i[1], 70, 70), 0)
                return i[2]
        return None
    
    def draw_move_option2(self, screen4, target):
        color = pygame.Color(50, 150, 50)
        result = cur.execute(f"""SELECT fraction FROM unit_stats WHERE name == '{target}'""").fetchall()
        result = int(result[0][0])
        for y in range(self.num1):
            for x in range(2):
                if self.list_per[y][x] == 0:
                    if result == 1:
                        pygame.draw.rect(screen4, color, (self.left + 350 + self.size_k1 * x + 1,
                            self.top + self.size_k1 * y + 1,
                            self.size_k1 - 2, self.size_k1 - 2), 0)
                        self.list_move[y][x] = True
                if self.list_per[y][self.num2 - x - 1] == 0:
                    if result != 1:
                        pygame.draw.rect(screen4, color, (self.left + 285 + self.size_k1 * (self.num2 - x) + 1,
                            self.top + self.size_k1 * (y) + 1,
                            self.size_k1 - 2, self.size_k1 - 2), 0)
                        self.list_move[y][self.num2 - x - 1] = True
        
    def make_pers(self, x, y, target):
        x -= (self.left + 350)
        y -= self.top
        x = x // self.size_k1
        y = y // self.size_k1
        self.list_move[y][x] = False
        self.list_per[y][x] = target
    
    def make_hod(self, data):
        hod = []
        for i in self.list_per:
            for j in i:
                if j != 0:
                    hod.append([j, int(data[j][0])])
        hod.sort(key = lambda i: i[1])
        for i in range(len(hod)):
            hod[i] = hod[i][0]
        return hod
    
    def pers(self, x, y):
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return self.list_per[y][x]
    
    def attack_option(self, x, y):
        x -= self.left
        y -= self.top
        x //= self.size_k
        y //= self.size_k
        result = cur.execute(f"""SELECT range FROM unit_stats WHERE name == '{self.list_per[y][x]}'""").fetchone()
        result = int(result[0]) + 1
        self.list_attack = []
        for i in range(self.num1):
            b = []
            for j in range(self.num2):
                b.append([i, j])
            self.list_attack.append(b)
        for i in range(self.num1):
            for j in range(self.num2):
                self.list_attack[i][j] = True
                if x >= j:
                    if y >= i and result <= x - j + y - i:
                        self.list_attack[i][j] = False
                    elif y < i and result <= x - j + i - y:
                        self.list_attack[i][j] = False
                else:
                    if y >= i and result <= j - x + y - i:
                        self.list_attack[i][j] = False
                    elif y < i and result <= j - x + i - y:
                        self.list_attack[i][j] = False
        for i in self.list_attack:
            for j in i:
                if j:
                    return j
        return False
    
    def draw_attack(self, screen2, x, y, target):
        x -= self.left
        y -= self.top
        x //= self.size_k
        y //= self.size_k
        color = pygame.Color(150, 50, 50)
        res0 = cur.execute(f"""SELECT fraction FROM unit_stats WHERE name == '{target}'""").fetchone()
        res0 = int(res0[0])
        if self.list_attack != [] and self.list_per != []:
            for i in range(self.num1):
                for j in range(self.num2):
                    if self.list_attack[i][j] is True and self.list_per[i][j] != 0 and target != self.list_per[i][j]:
                        res1 = cur.execute(f"""SELECT fraction FROM unit_stats WHERE name == '{self.list_per[i][j]}'""").fetchone()
                        res1 = int(res1[0])
                        if res0 != res1:
                            pygame.draw.rect(screen2, color, (self.left + self.size_k * j + 1,
                            self.top + self.size_k * i + 1,
                            self.size_k - 2, self.size_k - 2))
    
    def make_attack(self, target, data, x, y, hod):
        x -= self.left
        y -= self.top
        x //= self.size_k
        y //= self.size_k
        per = self.list_per[y][x]
        res0 = cur.execute(f"""SELECT * FROM unit_stats WHERE name == '{target}'""").fetchall()
        res0 = res0[0]
        res1 = cur.execute(f"""SELECT * FROM unit_stats WHERE name == '{per}'""").fetchall()
        res1 = res1[0]
        data[per][1] = int(data[per][1]) - (data[target][0] * int(res0[2]))
        data[per][0] = int(data[per][1]) // int((res1[1]))
        if data[per][1] % int((res1[1])) != 0:
            data[per][0] += 1
        if data[per][0] <= 0:
            self.list_per[y][x] = 0
            if per in hod:
                del hod[hod.index(per)]
        return [data, hod]
    
    def in_list_attack(self, x, y):
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return self.list_attack[y][x]

    
    def text_info(self, target, data):
        font = pygame.font.Font(None, 20)
        result = cur.execute(f"""SELECT * FROM unit_stats WHERE name == '{target}'""").fetchall()
        result = result[0]
        a = result[5][0]
        if a == 0:
            a = "Нежить"
        else:
            a = "Живые"
        return [f"Имя: {target}", f"Здоровье: {data[target][1]}",
                f"Атака: {int(result[2]) * int(data[target][0])}",
                f"Дальность атаки: {result[3]}", f"Количество: {data[target][0]}",
                f"Защита: {result[4]}", f"Скорость: {result[6]}", f"Фракция: {result[5]}"]
    
    def draw_button(self, screen, left, top):
        font = pygame.font.Font(None, 50)
        text = font.render("Завершить ход", True, (100, 255, 100))
        pygame.draw.rect(screen, (50, 150, 50), (left, top - 10, 280, 50), 1)
        screen.blit(text, (left + 8, top))
        

def load_image(name, colorkey=None):
    fullname = os.path.join('heroes_of_might_and_magic_pygame','data', name)
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