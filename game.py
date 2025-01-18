import pygame
from pygame.locals import *
import random

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0,10)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 500)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.move_ip(0, -10)

    def move_down(self):
        if self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 10)

    def move_left(self):
        if self.rect.left > 0:
            self.rect.move_ip(-10, 0)

    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(10, 0)

    # def update(self):
    #     pressed_keys = pygame.key.get_pressed()
    #     if self.rect.left > 0:
    #         if pressed_keys[K_LEFT]:
    #             self.rect.move_ip(-5, 0)
    #     if self.rect.right < SCREEN_WIDTH:
    #         if pressed_keys[K_RIGHT]:
    #             self.rect.move_ip(5, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

P1 = Player()
E1 = Enemy()

def play():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    P1.update()
    E1.move()

    DISPLAYSURF.fill(WHITE)
    P1.draw(DISPLAYSURF)
    E1.draw(DISPLAYSURF)

    pygame.display.update()
    FramePerSec.tick(FPS)

# while True:
#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()
#     P1.update()
#     E1.move()

#     DISPLAYSURF.fill(WHITE)
#     P1.draw(DISPLAYSURF)
#     E1.draw(DISPLAYSURF)

#     pygame.display.update()
#     FramePerSec.tick(FPS)