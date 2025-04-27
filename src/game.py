import pygame
from background import Background
from ground import Ground
from pipe import Pipe
from bird import Bird
from controls import Controls


class Game:
    RES = (1280, 720)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.RES)
        pygame.display.set_caption('FB')
        self.clock = pygame.time.Clock()
        self.running = True

        self.background = Background()
        self.ground = Ground()
        self.pipes = Pipe()
        self.bird = Bird()
        self.controls = Controls(self.bird)
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.controls.handle_input(event)

    def update(self):
        self.background.update()
        self.ground.update()
        self.pipes.update()
        self.bird.update()

        if self.bird.y + 18 >= self.screen.get_height() - 168:
            self.bird.alive = False
            self.bird.y = self.screen.get_height() - 168 - 18

        for pipe_pair in self.pipes.pipes:
            pipe_rect_top = pygame.Rect(pipe_pair[0]['x'], pipe_pair[0]['y'], 78, 480)
            pipe_rect_bottom = pygame.Rect(pipe_pair[1]['x'], pipe_pair[1]['y'], 78, 480)
            bird_rect = pygame.Rect(self.bird.x - 25, self.bird.y - 18, 51, 36)
            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                self.bird.alive = False

        for pipe_pair in self.pipes.pipes:
            if 'scored' not in pipe_pair[0]:
                pipe_pair[0]['scored'] = False
            if not pipe_pair[0]['scored'] and self.bird.x > pipe_pair[0]['x'] + 78:
                self.score += 1
                pipe_pair[0]['scored'] = True

    def draw(self):
        self.background.draw(self.screen)
        self.pipes.draw(self.screen)
        self.bird.draw(self.screen)
        self.ground.draw(self.screen)

        score_fmt = f'Score: {self.score}'
        score_surface = pygame.font.SysFont(None, 55).render(score_fmt, True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(self.screen.get_width() // 3, 22))
        self.screen.blit(score_surface, score_rect)
        pygame.display.flip()

    def show_game_over(self):
        self.draw()
        font = pygame.font.SysFont(None, 120)
        text_surface = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 60))
        self.screen.blit(text_surface, text_rect)

        font_small = pygame.font.SysFont(None, 60)
        restart_surface = font_small.render("Press Enter to restart", True, (255, 255, 255))
        restart_rect = restart_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 40))
        self.screen.blit(restart_surface, restart_rect)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return
            self.clock.tick(15)

    def run(self):
        while True:
            self.__init__()
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(60)
                if not self.bird.alive:
                    self.show_game_over()
                    break