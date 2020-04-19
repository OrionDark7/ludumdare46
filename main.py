import pygame, random
from pygame.math import Vector2
from game import *

"""
Orion's LD 46 Entry
Current File: main.py
"""


pygame.init()

window = pygame.display.set_mode([1280, 720])
pygame.display.set_caption("SECURITY")
window.fill([55, 55, 55])

click = 0

class Mouse(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([1,1])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0,0]
        self.buildat = [0,0]
        self.pos = [0,0]
        self.mask = pygame.mask.from_surface(self.image)
    def position(self):
        self.rect.left, self.rect.top = pygame.mouse.get_pos()
        self.pos  = pygame.mouse.get_pos()

tiles, lines = map.createmap()
gameobjects = pygame.sprite.Group()
viruses = pygame.sprite.Group()
tileselect = ["computer", "firewall", "antivirus"]
tile = 0
bitcoin = 10
tile_rotation = "left"
currenttile = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
currenttile.set_alpha(128)
currenttilerect = currenttile.get_rect()
currentrectpos = Vector2(currenttilerect.width/2, currenttilerect.height/2) + Vector2(64, 34)
router = objects.router()
pygame.time.set_timer(pygame.USEREVENT, 25)
pygame.time.set_timer(pygame.USEREVENT+1, 2000)

def createvirus():
    virus = entities.virus(random.choice(lines.sprites()).rect.center, random.choice(lines.sprites()).direction)
    viruses.add(virus)

def settile():
    global tile, tileselect, currenttile, currenttilerect, currentrectpos, tile_rotation
    currenttile = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
    currenttile.set_alpha(128)
    currenttilerect = currenttile.get_rect()
    currentrectpos = Vector2(currenttilerect.width / 2, currenttilerect.height / 2) + Vector2(64, 34)

mouse = Mouse()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if click == 1:
                if event.key == pygame.K_LEFT:
                    tile += 1
                    if tile > len(tileselect) - 1:
                        tile = 0
                    settile()
                if event.key == pygame.K_RIGHT:
                    tile -= 1
                    if tile < 0:
                        tile = len(tileselect) - 1
                    settile()
                if event.key == pygame.K_r:
                    if tile_rotation == "left":
                        tile_rotation = "right"
                    else:
                        tile_rotation = "left"
                    settile()
        if event.type == pygame.MOUSEMOTION:
            mouse.position()
            if click == 1:
                tiles.update("click", mouse)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.position()
            if click == 0:
                click = 1
            elif click == 1:
                click = 2
            if click == 2:
                tiles.update("click", mouse)
                if not mouse.buildat == [0,0]:
                    newobj = objects.object(mouse.buildat - currentrectpos, tileselect[tile] + "-" + tile_rotation)
                    gameobjects.add(newobj)
                    oldpos = mouse.pos
                    mouse.pos = newobj.rect.centerx, newobj.rect.centery
                    oldmask = mouse.mask
                    mouse.mask = newobj.mask
                    tiles.update("typeobject", mouse)
                    mouse.pos = oldpos
                    mouse.mask = oldmask
                    mouse.buildat = [0,0]
                    click = 0
        if event.type == pygame.USEREVENT:
            viruses.update(tiles, router)
        if event.type == pygame.USEREVENT+1:
            createvirus()

    window.fill([55, 55, 55])
    ui.text("BITCOIN - " + str(bitcoin), [5, 0], window)
    ui.text("ROUTER HEALTH - " + str(router.health), [5, 40], window)

    tiles.draw(window)
    gameobjects.draw(window)
    lines.draw(window)
    router.draw(window)
    viruses.draw(window)

    if click == 1:
        window.blit(currenttile, mouse.buildat - currentrectpos)

    pygame.display.flip()
pygame.quit()