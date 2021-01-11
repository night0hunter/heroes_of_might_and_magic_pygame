import pygame


class Menu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.text_x = 30
        self.text_y = 300
        self.flag = True
        self.color = 255

    def draw(self, screen, font):
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
