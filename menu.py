import pygame


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    running = True
    font = pygame.font.Font(None, 60)
    text_x = 30
    text_y = 300
    clock = pygame.time.Clock()
    FPS = 300
    color = 255
    flag = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if pygame.key.key_code("space") == pygame.K_SPACE:
                    running = False 
        screen.fill((0, 0, 0))
        text = font.render("Нажмите space, чтобы продолжить", True, (0, color, 0))
        screen.blit(text, (text_x, text_y))
        
        pygame.draw.rect(screen, (0, color, 0), (0, 0,
                                           800, 600), 10)
        pygame.display.flip()
        if flag:
            color -= 1

        elif not flag: 
            color += 1          
        
        if color == 255:
            flag = True
        elif color == 50:
            flag = False
        clock.tick(FPS)
    # завершение работы:
    pygame.quit()