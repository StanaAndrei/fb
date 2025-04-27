import pygame
from utils import ASSET_PATH

class Bird:
    def __init__(self):
        self.images = [
            pygame.image.load(ASSET_PATH('bird_down.png')).convert_alpha(),
            pygame.image.load(ASSET_PATH('bird_mid.png')).convert_alpha(),
            pygame.image.load(ASSET_PATH('bird_up.png')).convert_alpha()
        ]
        self.images = [pygame.transform.scale(img, (51, 36)) for img in self.images]
        self.x = 250
        self.y = 11
        self.velocity = 0
        self.gravity = 0.4
        self.jump_strength = -9
        self.alive = True
        self.current_image = 1
        self.animation_timer = 0
        self.animation_speed = 5
        self.max_rotation = 25
        self.min_rotation = -90
        self.rotation = 0

    def jump(self):
        if self.alive:
            self.velocity = self.jump_strength

    def update(self):
        if not self.alive:
            return
        self.velocity += self.gravity
        self.y += self.velocity
        if self.velocity < 0:
            self.rotation = self.max_rotation
        else:
            if self.rotation > self.min_rotation:
                self.rotation -= 3
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            if self.velocity > 0:
                self.current_image = 2
            elif self.velocity < 0:
                self.current_image = 0
            else:
                self.current_image = 1

    def draw(self, screen):
        image = self.images[self.current_image]
        rotated_image = pygame.transform.rotate(image, self.rotation)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        screen.blit(rotated_image, rect)