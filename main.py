import pygame
import pygame.gfxdraw
import random
import time
import asyncio
from math import sqrt

# Classes and functions
class Game:
    def __init__(self, circle_count: int, game_mode: str):
        self.round_time = 20
        self.hit_counter = 0
        self.start_time = time.time()
        self.circle_count = circle_count
        self.game_mode = game_mode
        if game_mode == 'moving':
            self.speed = 2  # Initial speed for moving targets
        else:
            self.speed = 0  # Static targets have no speed
        self.wave = Wave(circle_count, self.speed)

    def shoot(self, mouse_x, mouse_y):
        for circle in self.wave.circles:
            if sqrt((circle.x - mouse_x)**2 + (circle.y - mouse_y)**2) < circle.r:
                self.wave.circles.remove(circle)
                self.hit_counter += 1
                break

    def draw(self):
        for circle in self.wave.circles:
            circle.draw()

    def update(self):
        if len(self.wave.circles) == 0:
            self.speed += 1  # Increase speed for each new wave if moving
            self.wave = Wave(self.circle_count, self.speed)

class Wave:
    def __init__(self, circle_count, speed):
        self.circles = [Circle(speed) for x in range(circle_count)]

class Circle:
    def __init__(self, speed):
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(round(screen.get_height()*(1/3)), round(screen.get_height()*(2/3)))
        self.r = screen.get_height()/20
        self.vx = speed * random.choice([-1, 1])  # Horizontal velocity
        self.vy = speed * random.choice([-1, 1])  # Vertical velocity

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.r < 0 or self.x + self.r > screen.get_width():
            self.vx *= -1
        if self.y - self.r < 0 or self.y + self.r > screen.get_height():
            self.vy *= -1

    def draw(self):
        pygame.gfxdraw.aacircle(screen, self.x, self.y, round(self.r), text_color)
        pygame.gfxdraw.filled_circle(screen, self.x, self.y, round(self.r), text_color)

# Variables
pygame.display.set_caption("Aim Trainer")
screen = pygame.display.set_mode((1000, 500), pygame.RESIZABLE)
clock = pygame.time.Clock()
base_font_name = "Arial"
title_font = pygame.font.Font("Fredoka-Bold.ttf", size=round(screen.get_height()/10))
font = pygame.font.Font("Fredoka-Bold.ttf", size=round(screen.get_height()/20))
shot_sound = pygame.mixer.Sound("shot.wav")
bg_color = pygame.Color(170, 238, 187)
text_color = pygame.Color(85, 130, 139)
text_color_lighter = pygame.Color(159, 200, 208)
pygame.mouse.set_cursor(pygame.cursors.broken_x)

# Main function
async def main():
    running = True
    initialized = False
    game = None
    while running:
        if not initialized:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.fill(bg_color)
            title_text = title_font.render("Aim Trainer", True, text_color)
            title_text_rect = title_text.get_rect(center=(screen.get_width()/2, screen.get_height()/4))
            screen.blit(title_text, title_text_rect)
            start_text_left = font.render("Click this side for static targets", True, text_color)
            start_text_left_rect = start_text_left.get_rect(center=(screen.get_width()/4, screen.get_height()/2))
            screen.blit(start_text_left, start_text_left_rect)
            start_text_right = font.render("Click this side for moving targets", True, text_color)
            start_text_right_rect = start_text_right.get_rect(center=(screen.get_width()*(3/4), screen.get_height()/2))
            screen.blit(start_text_right, start_text_right_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_mode = 'moving' if event.pos[0] > screen.get_width() / 2 else 'static'
                    game = Game(5, game_mode)
                    initialized = True
            pygame.display.flip()
            await asyncio.sleep(0.01)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.shoot(event.pos[0], event.pos[1])
            if game.game_mode == 'moving':
                for circle in game.wave.circles:
                    circle.update()
            screen.fill(bg_color)
            game.draw()
            game.update()
            pygame.display.flip()
            if (time.time() - game.start_time) > game.round_time:
                game = None
                initialized = False
            await asyncio.sleep(0.01)

# Run the main function
asyncio.run(main())
