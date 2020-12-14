class Cursor(pygame.sprite.Sprite):
    image = load_image("arrow.png")
    image_arrow = load_image("arrow.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Cursor.image
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width)
        self.rect.y = random.randrange(height)

    def update(self, *args):
        self.image = self.image_arrow
        