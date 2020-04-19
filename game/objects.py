import pygame
from pygame.math import Vector2

"""
Orion's LD 46 Entry
Current File: /game/objects.py
"""

pygame.init()
pygame.mixer.init()

sounds = {"action" : pygame.mixer.Sound("./resources/sfx/action.wav"), "explosion" : pygame.mixer.Sound("./resources/sfx/explosion.wav"), "nextwave" : pygame.mixer.Sound("./resources/sfx/nextwave.wav"), "shoot" : pygame.mixer.Sound("./resources/sfx/shoot.wav")}

def calculateoffset(obj1, obj2):
    return (obj1.rect.left - obj2.rect.left), (obj1.rect.top - obj2.rect.top)

class tile(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/tile.png")
        self.rect = self.image.get_rect()
        self.rect.center = list(position)
        self.type = "alive"
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, action, mouse):
        if action == "click" and not self.type == "dead":
            if self.rect.collidepoint(mouse.pos):
                mouse.buildat = Vector2(self.rect.centerx, self.rect.centery)
        if action == "typeobject":
            if self.mask.overlap_area(mouse.mask, calculateoffset(self, mouse)):
                self.settype("object")
    def settype(self, type):
        if type == "dead":
            if self.type == "alive":
                self.type = "dead"
                self.image = pygame.image.load("./resources/images/tile-dead.png")
        if type == "object":
            if self.type == "alive":
                self.type = "object"
                self.image = pygame.image.load("./resources/images/tile-object.png")

class object(pygame.sprite.Sprite):
    def __init__(self, position, type):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/"+type+".png")
        self.rect = self.image.get_rect()
        self.rect.center = list(position)
        self.mask = pygame.mask.from_surface(self.image)
        self.type = type.split("-")[0]
        self.direction = type.split("-")[1]
        self.tick = 0
    def update(self, bulletgrp):
        self.tick += 1
        if self.type == "antivirus" and self.tick > 100:
            newbullet = bullet(self.rect.center, self.direction)
            bulletgrp.add(newbullet)
            self.tick = 0
        elif not self.type == "antivirus":
            pygame.sprite.spritecollide(self, bulletgrp, True)

class bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = list(position)
        if direction == "left":
            self.velocity = Vector2(-2, 1)
        if direction == "right":
            self.velocity = Vector2(2, 1)
    def update(self):
        self.rect.center += self.velocity
        if self.rect.centerx > 1280 or self.rect.left < 0:
            self.kill()
        if self.rect.centery > 720 or self.rect.centery < 0:
            self.kill()

class line(pygame.sprite.Sprite):
    def __init__(self, position, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/line-"+str(dir)+".png")
        self.rect = self.image.get_rect()
        self.rect.center = list(position)
        self.direction = dir
        self.mask = pygame.mask.from_surface(self.image)

class router(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/router.png")
        self.rect = self.image.get_rect()
        self.rect.center = 660, 400
        self.health = 100
        self.mask = pygame.mask.from_surface(self.image)
    def draw(self, window):
        window.blit(self.image, [self.rect.left, self.rect.top])