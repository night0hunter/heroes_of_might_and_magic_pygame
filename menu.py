import pygame


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.text_x = 30
        self.text_y = 300
        self.flag = True
        self.color = 255

    def draw(self, screen):
        screen.fill((0, 0, 0))
        text = font.render("Нажмите space, чтобы продолжить", True, (0, self.color, 0))
        screen.blit(text, (self.text_x, self.text_y))
        pygame.draw.rect(screen, (0, self.color, 0), (0, 0, 800, 600), 10)
        pygame.display.flip()
        if self.flag:
            self.color -= 1
        elif not self.flag: 
            self.color += 1          
        
        if self.color == 255:
            self.flag = True
        elif self.color == 50:
            self.flag = False

if __name__ == '__main__':
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
            if event.type == pygame.KEYDOWN:
                if pygame.key.key_code("space") == pygame.K_SPACE:
                    running = False 
        a.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    # завершение работы:
    pygame.quit()