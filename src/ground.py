import pygame
from utils import ASSET_PATH

class Ground:
    def __init__(self):
        self.image = pygame.image.load(ASSET_PATH('base.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (1280, 168))
        self.width = self.image.get_width()
        self.scroll = 0
        self.speed = 4

    def update(self):
        self.scroll -= self.speed
        if self.scroll <= -self.width:
            self.scroll = 0

    def draw(self, screen):
        y_pos = screen.get_height() - self.image.get_height()
        screen.blit(self.image, (self.scroll, y_pos))
        screen.blit(self.image, (self.scroll + self.width, y_pos))