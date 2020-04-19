import pygame, random
from pygame.math import Vector2

"""
Orion's LD 46 Entry
Current File: /game/entities.py
"""

pygame.init()
pygame.mixer.init()

font = pygame.font.Font("./resources/Pixeled.ttf", 8)

sounds = {"action" : pygame.mixer.Sound("./resources/sfx/action.wav"), "explosion" : pygame.mixer.Sound("./resources/sfx/explosion.wav"), "nextwave" : pygame.mixer.Sound("./resources/sfx/nextwave.wav"), "shoot" : pygame.mixer.Sound("./resources/sfx/shoot.wav")}

def calculateoffset(obj1, obj2):
    return (obj1.rect.left - obj2.rect.left), (obj1.rect.top - obj2.rect.top)

class virus(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/virus.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.mask = pygame.mask.from_surface(self.image)
        self.goingto = 660, 264
        if direction == "right":
            self.velocity = Vector2(-2, -1)
        elif direction == "left":
            self.velocity = Vector2(2, -1)
    def update(self, tiles, router, bulletgrp, effectgrp, mouse):
        self.rect.center += self.velocity
        vx, vy = 0, 0
        if pygame.sprite.spritecollide(self, bulletgrp, True):
            self.kill()
            sounds["shoot"].play()
            profit = random.randint(2,4)
            mouse.profit += profit
            neweffect = effects(self.rect.center, "+"+str(profit)+"B", color=[255, 225, 0])
            effectgrp.add(neweffect)
        if pygame.sprite.spritecollide(self, tiles, False):
            if self.rect.centerx < self.goingto[0]:
                vx = 2
            elif self.rect.centerx > self.goingto[0]:
                vx = -2
            if self.rect.centery < self.goingto[1]:
                vy = 1
            elif self.rect.centery > self.goingto[1]:
                vy = -1
            self.velocity = Vector2(vx, vy)
            for tile in tiles:
                if not self.mask.overlap_area(tile.mask, calculateoffset(tile, self)) == 0:
                    tile.settype("dead")
            if not self.mask.overlap_area(router.mask, calculateoffset(router, self)) == 0:
                self.kill()
                sounds["explosion"].play()
                router.health -= 2
                neweffect = effects(self.rect.center, "-2 HEALTH", color=[188, 28, 36])
                effectgrp.add(neweffect)

class effects(pygame.sprite.Sprite):
    def __init__(self, position, param, image=False, color=[255, 255, 255]):
        pygame.sprite.Sprite.__init__(self)
        if image:
            self.image = pygame.image.load(param)
        else:
            self.image = font.render(param, 1, color)
        self.originalimg = self.image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.velocity = Vector2(0, -1)
        self.alphavalue = 0
    def update(self):
        self.alphavalue += 5
        if self.alphavalue > 255:
            self.kill()
        self.image.set_alpha(255 - self.alphavalue)
        self.rect.center += self.velocity
