import pygame

class Controls:
    def __init__(self, bird):
        self.bird = bird

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.jump()