import pygame
from pygame.math import Vector2

class tile(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/tile.png")
        self.rect = self.image.get_rect()
        self.rect.center = list(position)
    def update(self, action, map, mouse):
        if action == "click":
            if self.rect.collidepoint(mouse.pos):
                mouse.buildat = Vector2(self.rect.centerx, self.rect.centery)

class computer(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/computer.png")
        self.rect = self.image.get_rect()
        self.rect.center = list(position)