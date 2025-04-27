import pygame
from utils import ASSET_PATH

class Background:
    def __init__(self):
        self.image = pygame.image.load(ASSET_PATH('bg.png')).convert()
        self.image = pygame.transform.scale(self.image, (1280, 720))
        self.width = self.image.get_width()
        self.scroll = 0
        self.speed = 1

    def update(self):
        self.scroll -= self.speed
        if self.scroll <= -self.width:
            self.scroll = 0

    def draw(self, screen):
        screen.blit(self.image, (self.scroll, 0))
        screen.blit(self.image, (self.scroll + self.width, 0))