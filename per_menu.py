import pygame as pg


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('white')
COLOR_ACTIVE = pg.Color('white')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_1 or event.key == pg.K_2 or event.key == pg.K_3 or event.key == pg.K_4\
                    or event.key == pg.K_5 or event.key == pg.K_6 or event.key == pg.K_7\
                    or event.key == pg.K_8 or event.key == pg.K_9 or event.key == pg.K_0\
                    or event.key == pg.K_BACKSPACE:
                if self.active:
                    if event.key == pg.K_RETURN:
                        print(self.text)
                        self.text = ''
                    elif event.key == pg.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif len(self.text) <= 2:
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.color)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

    def read_text(self):
        return self.text
