import pygame, random
from konst import RES
from utils import ASSET_PATH

class Pipe:
    def __init__(self):
        self.pipe_image = pygame.image.load(ASSET_PATH('pipe.png')).convert_alpha()
        self.pipe_image = pygame.transform.scale(self.pipe_image, (78, 480))
        self.pipe_image_top = pygame.transform.rotate(self.pipe_image, 180)
        self.GAP = 300
        self.speed = 4
        self.pipes = []
        self.spawn_timer = 0
        self.spawn_interval = 90

    def spawn_pipe(self):
        screen_height = RES[1]
        pipe_height = self.pipe_image.get_height()
        gap_size = self.GAP
        min_gap_y = 50
        max_gap_y = screen_height - gap_size - 50
        gap_y = random.randint(min_gap_y, max_gap_y)
        pipe_top = {'x': 1280, 'y': gap_y - pipe_height}
        pipe_bottom = {'x': 1280, 'y': gap_y + gap_size}
        self.pipes.append((pipe_top, pipe_bottom))

    def update(self):
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_pipe()
            self.spawn_timer = 0
        for pipe_pair in self.pipes:
            pipe_pair[0]['x'] -= self.speed
            pipe_pair[1]['x'] -= self.speed
        self.pipes = [pipe for pipe in self.pipes if pipe[0]['x'] > -100]

    def draw(self, screen):
        for pipe_pair in self.pipes:
            screen.blit(self.pipe_image_top, (pipe_pair[0]['x'], pipe_pair[0]['y']))
            screen.blit(self.pipe_image, (pipe_pair[1]['x'], pipe_pair[1]['y']))