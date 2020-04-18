import pygame
from game import objects

pygame.init()

def createmap():
    tiles = pygame.sprite.Group()
    for j in range(10):
        for i in range(10):
            obj = objects.tile([(i+20-j)*33, (i+15+j)*17])
            tiles.add(obj)
    return tiles