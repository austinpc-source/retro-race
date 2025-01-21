import pygame
from pygame.locals import *
import random

pygame.init()

# Predefined some colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 60
 
# Screen information
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


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

    def move_left(self):
        if self.rect.left > 0:
            self.rect.move_ip(-20, 0)

    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(20, 0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Game:
    def __init__(self):
        try:
            print("Initializing Game")
            self.DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            pygame.display.set_caption("Game")
            self.clock = pygame.time.Clock()
            self.P1 = Player()
            self.E1 = Enemy()
            print("Finished Initializing Game")
        except Exception as e:
            print(f"Error during Game initialization: {e}")
       
    def play(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
        self.P1.update()
        self.E1.move()
        self.DISPLAYSURF.fill(WHITE)
        self.P1.draw(DISPLAYSURF)
        self.E1.draw(DISPLAYSURF)
        pygame.display.update()
        self.clock.tick(FPS)
