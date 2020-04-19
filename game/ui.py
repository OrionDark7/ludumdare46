import pygame

"""
Orion's LD 46 Entry
Current File: /game/ui.py.py
"""

pygame.init()

font = pygame.font.Font("./resources/Pixeled.ttf", 18)

def fontSize(size):
    global font
    font = pygame.font.Font("./resources/Pixeled.ttf", int(size))

def text(text, pos, window):
    render = font.render(str(text), 1, [255, 255, 255])
    window.blit(render, pos)
