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

def text(text, pos, window, color=[255, 255, 255]):
    render = font.render(str(text), 1, color)
    window.blit(render, pos)

def centertext(text, pos, window, color=[255, 255, 255]):
    render = font.render(str(text), 1, color)
    rect = render.get_rect()
    window.blit(render, [pos[0]-rect.width/2, pos[1]])

class button(pygame.sprite.Sprite):
    def __init__(self, text, pos):
        global font
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(str(text), 1, [255, 255, 255])
        self.text = text
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pos
    def click(self, mouse):
        clicked = False
        if self.rect.colliderect(mouse.rect):
            clicked = True
        return clicked
    def update(self, mouse):
        if self.rect.collidepoint(mouse.rect.topleft):
            self.image = font.render(str(self.text), 1, [255, 255, 255])
        else:
            self.image = font.render(str(self.text), 1, [170, 170, 170])