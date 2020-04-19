import pygame, random
from game import objects

"""
Orion's LD 46 Entry
Current File: /game/map.py
"""

pygame.init()

def createmap():
    tiles = pygame.sprite.Group()
    lines = pygame.sprite.Group()
    for j in range(10):
        for i in range(10):
            obj = objects.tile([(i+20-j)*33, (i+15+j)*17])
            tiles.add(obj)
    for l in range(1):
        if random.randint(0, 1) == 0:
            i = random.randint(0, 9)
            for e in range(15):
                obj = objects.line([(i + 20 - (e+10.5)) * 33, (i + 15 + (e+10.5)) * 17], "left")
                lines.add(obj)
        else:
            i = random.randint(0, 9) + 10
            for e in range(10):
                obj = objects.line([((e+15) + 25.5 - i) * 33, ((e+10.5) + 5 + i) * 17], "right")
                lines.add(obj)

    return tiles, lines