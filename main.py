import pygame
import asyncio
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

    def shoot(self, mouse_x, mouse_y):
        for circle in self.wave.circles:
            if sqrt((circle.x - mouse_x)**2 + (circle.y - mouse_y)**2) < circle.r:
                self.wave.circles.remove(circle)
                shot_sound.stop()
                shot_sound.play()
                self.hit_counter += 1

    def draw(self):
        for circle in self.wave.circles:
            circle.draw()
        timer_text = font.render(str(round(self.round_time - (time.time() - self.start_time))), True, text_color)
        timer_rect = timer_text.get_rect(center=(screen.get_width()/2, 0))
        screen.blit(timer_text, (timer_rect[0], timer_rect[1] + timer_rect.height/2))

    def update(self):
        if len(self.wave.circles) == 0:
            self.speed += 1 if self.game_mode == 'moving' else 0
            self.wave = Wave(self.circle_count, self.speed)

class Wave:
    def __init__(self, circle_count, speed):
        self.circle_count = circle_count
        self.circles = [Circle(speed) for _ in range(circle_count)]

class Circle:
    def __init__(self, speed):
        self.x = random.randint(0, screen.get_width())
        self.y = random.randint(round(screen.get_height()*(1/3)), round(screen.get_height()*(2/3)))
        self.r = screen.get_height()/20
        self.vx = speed * random.choice([-1, 1])
        self.vy = speed * random.choice([-1, 1])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x - self.r < 0 or self.x + self.r > screen.get_width():
            self.vx *= -1
        if self.y - self.r < 0 or self.y + self.r > screen.get_height():
            self.vy *= -1

    def draw(self):
        pygame.draw.circle(screen, text_color, (self.x, self.y), self.r)

# Variables
pygame.display.set_caption("Aim Trainer")
screen = pygame.display.set_mode((1000,500), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", round(screen.get_height()/20))
shot_sound = pygame.mixer.Sound("shot.wav")
bg_color = pygame.Color(170, 238, 187)
text_color = pygame.Color(85, 130, 139)

async def main():
    running = True
    initialized = False
    game = None
    while running:
        if not initialized:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            screen.fill(bg_color)
            start_text = font.render("Click to start", True, text_color)
            text_rect = start_text.get_rect(center=(screen.get_width()/2, screen.get_height()/2))
            screen.blit(start_text, text_rect)
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

asyncio.run(main())
