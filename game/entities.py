import pygame
from pygame.math import Vector2

pygame.init()

def calculateoffset(obj1, obj2):
    return (obj1.rect.left - obj2.rect.left), (obj1.rect.top - obj2.rect.top)

class virus(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("./resources/images/virus.png")
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.mask = pygame.mask.from_surface(self.image)
        if direction == "right":
            self.velocity = Vector2(-2, -1)
        elif direction == "left":
            self.velocity = Vector2(2, -1)
    def update(self, tiles, router):
        self.rect.center += self.velocity
        vx, vy = 0, 0
        if pygame.sprite.spritecollide(self, tiles, False):
            if self.rect.centerx < 660:
                vx = 2
            elif self.rect.centerx > 660:
                vx = -2
            if self.rect.centery < 400:
                vy = 1
            elif self.rect.centery > 400:
                vy = -1
            self.velocity = Vector2(vx, vy)
            for tile in tiles:
                if not self.mask.overlap_area(tile.mask, calculateoffset(tile, self)) == 0:
                    tile.settype("dead")
            if not self.mask.overlap_area(router.mask, calculateoffset(router, self)) == 0:
                self.kill()
                router.health -= 2