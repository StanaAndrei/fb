import pygame, random
from time import time

ASSET_PATH = lambda s: './assets/' + s

class Game:
    RES = (1280, 720)

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(Game.RES)
        pygame.display.set_caption('FB')
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize game objects
        self.background = Background()
        self.ground = Ground()
        self.pipes = Pipe()
        self.bird = Bird()  # Add bird
        self.controls = Controls(self.bird)  # Add controls

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

        # Basic collision detection with ground
        if self.bird.y + 18 >= self.screen.get_height() - 168:  # 168 is ground height
            self.bird.alive = False
            self.bird.y = self.screen.get_height() - 168 - 18  # Place bird on ground

        # Basic collision detection with pipes
        for pipe_pair in self.pipes.pipes:
            pipe_rect_top = pygame.Rect(
                pipe_pair[0]['x'],
                pipe_pair[0]['y'],
                78,  # pipe width
                480  # pipe height
            )
            pipe_rect_bottom = pygame.Rect(
                pipe_pair[1]['x'],
                pipe_pair[1]['y'],
                78,  # pipe width
                480  # pipe height
            )
            bird_rect = pygame.Rect(
                self.bird.x - 25,
                self.bird.y - 18,
                51,  # bird width
                36   # bird height
            )

            if bird_rect.colliderect(pipe_rect_top) or bird_rect.colliderect(pipe_rect_bottom):
                self.bird.alive = False

        # --- Score calculation: increment score when bird passes a pipe ---
        for pipe_pair in self.pipes.pipes:
            # Add a 'scored' flag to each pipe_pair if it doesn't exist
            if 'scored' not in pipe_pair[0]:
                pipe_pair[0]['scored'] = False

            # Check if bird has passed the pipe and it hasn't been scored yet
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
                        return  # Signal to restart
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

class Pipe:
    def __init__(self):
        self.pipe_image = pygame.image.load(ASSET_PATH('pipe.png')).convert_alpha()
        self.pipe_image = pygame.transform.scale(self.pipe_image, (78, 480))
        self.pipe_image_top = pygame.transform.rotate(self.pipe_image, 180)

        # Pipe properties
        self.GAP = 300  # Gap between pipes
        self.speed = 4
        self.pipes = []
        self.spawn_timer = 0
        self.spawn_interval = 90  # Frames between pipe spawns

    def spawn_pipe(self):
        screen_height = Game.RES[1]
        pipe_height = self.pipe_image.get_height()
        gap_size = self.GAP

        # Calculate the minimum and maximum y for the top of the gap
        min_gap_y = 50  # Padding from the top
        max_gap_y = screen_height - gap_size - 50  # Padding from the bottom

        # Random y position for the gap (top of the gap)
        gap_y = random.randint(min_gap_y, max_gap_y)

        # Create pipe positions (x, y) for top and bottom pipes
        pipe_top = {
            'x': 1280,
            'y': gap_y - pipe_height
        }
        pipe_bottom = {
            'x': 1280,
            'y': gap_y + gap_size
        }
        self.pipes.append((pipe_top, pipe_bottom))

    def update(self):
        # Spawn new pipes
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_pipe()
            self.spawn_timer = 0

        # Update pipe positions
        for pipe_pair in self.pipes:
            pipe_pair[0]['x'] -= self.speed
            pipe_pair[1]['x'] -= self.speed

        # Remove pipes that are off-screen
        self.pipes = [pipe for pipe in self.pipes if pipe[0]['x'] > -100]

    def draw(self, screen):
        for pipe_pair in self.pipes:
            screen.blit(self.pipe_image_top, (pipe_pair[0]['x'], pipe_pair[0]['y']))
            screen.blit(self.pipe_image, (pipe_pair[1]['x'], pipe_pair[1]['y']))


class Bird:
    def __init__(self):
        self.images = [
            pygame.image.load(ASSET_PATH('bird_down.png')).convert_alpha(),
            pygame.image.load(ASSET_PATH('bird_mid.png')).convert_alpha(),
            pygame.image.load(ASSET_PATH('bird_up.png')).convert_alpha()
        ]

        # Scale bird images (adjust size as needed for your assets)
        self.images = [pygame.transform.scale(img, (51, 36)) for img in self.images]

        self.x = 250  # Fixed x position
        self.y = 11  # Starting y position
        self.velocity = 0
        self.gravity = 0.4
        self.jump_strength = -9
        self.alive = True

        self.current_image = 1  # Start with middle image
        self.animation_timer = 0
        self.animation_speed = 5  # Frames between animation updates

        self.max_rotation = 25  # Maximum rotation angle
        self.min_rotation = -90  # Minimum rotation angle
        self.rotation = 0

    def jump(self):
        if self.alive:
            self.velocity = self.jump_strength

    def update(self):
        if not self.alive:
            return

        # Apply gravity and update position
        self.velocity += self.gravity
        self.y += self.velocity

        # Update rotation based on velocity
        if self.velocity < 0:
            self.rotation = self.max_rotation
        else:
            if self.rotation > self.min_rotation:
                self.rotation -= 3

        # Animate the bird
        self.animation_timer += 1
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            # If bird is falling, use falling animation
            if self.velocity > 0:
                self.current_image = 2  # bird_down
            elif self.velocity < 0:
                self.current_image = 0  # bird_up
            else:
                self.current_image = 1  # bird_middle

    def draw(self, screen):
        # Get current image
        image = self.images[self.current_image]

        # Rotate image
        rotated_image = pygame.transform.rotate(image, self.rotation)

        # Get rect for centered rotation
        rect = rotated_image.get_rect(center=(self.x, self.y))

        # Draw the bird
        screen.blit(rotated_image, rect)

class Controls:
    def __init__(self, bird):
        self.bird = bird

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.bird.jump()

if __name__ == '__main__':
    random.seed(int(time() % 100))
    game = Game()
    game.run()