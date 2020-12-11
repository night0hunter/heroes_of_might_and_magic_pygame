import pygame


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
        self.size_k = 50
        self.top = 50
        self.left = 50

    def setting(self, left, top, size):
        self.left = left
        self.top = top
        self.size_k = size

    def draw(self, color):
        for i in range(self.num):
            for j in range(self.num):
                pygame.draw.rect(screen, pygame.Color(str(color)),
                                (self.left + self.size_k * j, self.top + self.size_k * i,
                                 self.size_k, self.size_k), 1)
    def move_option(self, coord_x, coord_y):
        x, y = coord_x, coord_y
        x -= self.left
        y -= self.top
        x = x // self.size_k
        y = y // self.size_k
        return (x, y)
    def in_board(self, coord_x, coord_y):
        if self.left <= coord_x <= self.left + self.size_k * self.num:
            if self.top <= coord_y <= self.top + self.size_k * self.num:
                return True
        return False
            
size = 800, 600
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))
a = Board(size[0], size[1], 8)
a.setting(10, 10, 50)
a.draw("white")
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.key_code("space") == pygame.K_SPACE:
                print("hello")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if in_board(event.pos[0], event.pos[1]):


    pygame.display.flip()

pygame.quit()