import pygame
import pygame.gfxdraw
import random
import time
from math import sqrt

pygame.init()
pygame.font.init()
pygame.mixer.init()

# Classes and functions
class Game:
    def __init__(self, circle_count: int, game_mode: str):
        self.round_time = 20
        self.hit_counter = 0
        self.start_time = time.time()
        self.wavetimes = []
        self.circle_count = circle_count
        self.game_mode = game_mode
        if game_mode == 'moving':
            self.speed = 2  # Initial speed for moving targets
        else:
            self.speed = 0  # Static targets have no speed
        self.wave = Wave(circle_count, self.speed)

    def shoot(self):
        # Handles shooting
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for circle in self.wave.circles:
            if sqrt((circle.x - mouse_x)**2 + (circle.y - mouse_y)**2) < circle.r:
                self.wave.circles.remove(circle)
                shot_sound.stop() # Stop previously playing sound
                shot_sound.play() # Play sound
                self.hit_counter += 1
                break

    def draw(self):
        # Draws wave circles
        for circle in self.wave.circles:
            circle.draw()

        # Draw timer
        timer_text = font.render(str(round(self.round_time - (time.time() - self.start_time))), True, text_color)
        timer_rect = timer_text.get_rect(center=(screen.get_width()/2, 0))
        screen.blit(timer_text, (timer_rect[0], timer_rect[1] + timer_rect.height/2))

        # Reset tooltip
        reset_text = font.render("Press r to reset", True, text_color)
        reset_text_rect = reset_text.get_rect(center=(screen.get_width()/2, screen.get_height()))
        screen.blit(reset_text, (reset_text_rect[0], reset_text_rect[1] - reset_text_rect.height/2))

    def update(self):
        # Reinitializes wave if wave is empty
        if len(self.wave.circles) == 0:
            self.speed += 1  # Increase speed for each new wave if moving
            wavetime = time.time() - self.wave.start_time
            self.wavetimes.append(wavetime)
            self.wave = Wave(self.circle_count, self.speed)

class Wave:
    def __init__(self, circle_count, speed):
        self.start_time = time.time()
        self.circle_count = circle_count
        self.circles = [Circle(speed) for x in range(circle_count)]

class Circle:
    def __init__(self, speed):
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(round(screen.get_height()*(1/3)), round(screen.get_height()*(2/3)))
        self.r = screen.get_height()/20
        self.vx = speed * random.choice([-1, 1])  # Horizontal velocity
        self.vy = speed * random.choice([-1, 1])  # Vertical velocity

    def update(self):
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy
        # Bounce off the edges of the screen
        if self.x - self.r < 0 or self.x + self.r > screen.get_width():
            self.vx *= -1
        if self.y - self.r < 0 or self.y + self.r > screen.get_height():
            self.vy *= -1

    def draw(self):
        pygame.gfxdraw.aacircle(screen, self.x, self.y, round(self.r), text_color)
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, round(self.r), text_color)

# Variables
pygame.display.set_caption("Aim Trainer")
screen = pygame.display.set_mode((1000,500), pygame.RESIZABLE)
clock = pygame.time.Clock()
base_font_name = "Arial"
title_font = pygame.font.Font("Fredoka-Bold.ttf", size=round(screen.get_height()/10))
font = pygame.font.Font("Fredoka-Bold.ttf", size=round(screen.get_height()/20))
shot_sound = pygame.mixer.Sound("shot.wav")
bg_color = pygame.Color(170, 238, 187)
text_color = pygame.Color(85, 130, 139)
text_color_lighter = pygame.Color(159, 200, 208)
pygame.mouse.set_cursor(pygame.cursors.broken_x)

# Main game loop
running = True
initialized = False
game_mode = None  # Static or Moving

while running:
    # Initializing
    if not initialized:
        # Gets mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Fills screen
        screen.fill(bg_color)

        # Title text
        title_text = title_font.render("Aim Trainer", True, text_color)
        title_text_rect = title_text.get_rect(center=(screen.get_width()/2, screen.get_height()/4))
        screen.blit(title_text, title_text_rect)

        # Left initializer text
        start_text_left = font.render("Click this side for static targets", True, text_color)
        start_text_left_rect = start_text_left.get_rect(center=(screen.get_width()/4, screen.get_height()/2))
        screen.blit(start_text_left, start_text_left_rect)

        # Right initializer text
        start_text_right = font.render("Click this side for moving targets", True, text_color)
        start_text_right_rect = start_text_right.get_rect(center=(screen.get_width()*(3/4), screen.get_height()/2))
        screen.blit(start_text_right, start_text_right_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_text_left_rect.collidepoint(event.pos):
                    game_mode = 'static'
                    game = Game(5, game_mode)  # Adjust number of targets as needed
                    initialized = True
                elif start_text_right_rect.collidepoint(event.pos):
                    game_mode = 'moving'
                    game = Game(5, game_mode)  # Adjust number of targets as needed
                    initialized = True

        pygame.display.flip()
        clock.tick(60)

    # Main game loop
    if running and initialized:
        # Event checking
        for event in pygame.event.get():
            # Exits the loop when window is closed
            if event.type == pygame.QUIT:
                running = False

            # Shoots
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.shoot()

            # Reset button
            if pygame.key.get_pressed()[pygame.K_r]:
                initialized = False
                break

        if game_mode == 'moving':
            # Update each circle's position if the game mode is moving
            for circle in game.wave.circles:
                circle.update()

        # Fills screen with background color
        screen.fill(bg_color)

        # Updates the game
        game.draw()
        game.update()

        # Reinitializes game if time is up
        if (time.time() - game.start_time) > game.round_time:
            end_game_string = f"Circles: {game.hit_counter}"
            end_game_text = font.render(end_game_string, True, text_color)
            end_game_rect = end_game_text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
            pygame.draw.rect(screen, bg_color, end_game_rect)
            screen.blit(end_game_text, end_game_rect)
            pygame.display.update(end_game_rect) 
            time.sleep(1)
            pygame.event.clear()
            initialized = False

        # Renders whole screen
        pygame.display.flip()

        # Lock fps
        clock.tick(60)

# Quits game
pygame.quit()
