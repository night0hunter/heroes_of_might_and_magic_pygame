import pygame


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    running = True
    font = pygame.font.Font(None, 60)
    text_x = 30
    text_y = 300
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.key_code("space") == pygame.K_SPACE:
                    running = False 
            
        for i in range(255, 50, -1):    
            screen.fill((0, 0, 0))
            text = font.render("Нажмите space, чтобы продолжить", True, (0, i, 0))
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()

        for i in range(50, 256, 1):
            screen.fill((0, 0, 0))
            text = font.render("Нажмите space, чтобы продолжить", True, (0, i, 0))
            screen.blit(text, (text_x, text_y))
            pygame.display.flip()
    # завершение работы:
    pygame.quit()