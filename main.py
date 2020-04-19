import pygame, random
from pygame.math import Vector2
from game import *

"""
Orion's LD 46 Entry
Current File: main.py
"""


pygame.init()
pygame.mixer.init()

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
turrents = pygame.sprite.Group()
bullets = pygame.sprite.Group()
viruses = pygame.sprite.Group()
gamebuttons = pygame.sprite.Group()
wavebutton = ui.button("START WAVE 1", [5, 670])
gamebuttons.add(wavebutton)
tileselect = ["computer", "firewall", "antivirus", "server"]
tile = 0
bitcoin = 10
wave = 0
wavestarted = False
tile_rotation = "left"
currenttile = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
currenttile.set_alpha(128)
currenttilerect = currenttile.get_rect()
waves = [5, 10, 20, 25, 40, 50]
virusescreated = 0
virusestocreate = 0
currentrectpos = Vector2(currenttilerect.width/2, currenttilerect.height/2)
router = objects.router()
pygame.time.set_timer(pygame.USEREVENT, 25)
pygame.time.set_timer(pygame.USEREVENT+1, 2000)
pygame.time.set_timer(pygame.USEREVENT+2, 500)

sounds = {"action" : pygame.mixer.Sound("./resources/sfx/action.wav"), "explosion" : pygame.mixer.Sound("./resources/sfx/explosion.wav"), "nextwave" : pygame.mixer.Sound("./resources/sfx/nextwave.wav"), "shoot" : pygame.mixer.Sound("./resources/sfx/shoot.wav")}

def createvirus():
    virus = entities.virus(random.choice(lines.sprites()).rect.center, random.choice(lines.sprites()).direction)
    viruses.add(virus)

def settile():
    global tile, tileselect, currenttile, currenttilerect, currentrectpos, tile_rotation
    currenttile = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
    currenttile.set_alpha(128)
    currenttilerect = currenttile.get_rect()
    currentrectpos = Vector2(currenttilerect.width / 2, currenttilerect.height / 2)

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
                    sounds["action"].play()
                if event.key == pygame.K_RIGHT:
                    tile -= 1
                    if tile < 0:
                        tile = len(tileselect) - 1
                    settile()
                    sounds["action"].play()
                if event.key == pygame.K_r:
                    if tile_rotation == "left":
                        tile_rotation = "right"
                    else:
                        tile_rotation = "left"
                    settile()
                    sounds["action"].play()
        if event.type == pygame.MOUSEMOTION:
            mouse.position()
            if click == 1:
                tiles.update("click", mouse)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.position()
            print(pygame.mouse.get_pressed())
            if pygame.mouse.get_pressed()[0] == 1:
                if wavebutton.click(mouse):
                    wavestarted = True
                    wave += 1
                    virusescreated = 0
                    try:
                        virusestocreate = waves[wave-1]
                    except:
                        virusestocreate = 50 + (10 * (wave-5))
                    wavebutton.text = "WAVE STARTED"
                elif click == 1:
                    click = 2
                    sounds["action"].play()
                if click == 2:
                    tiles.update("click", mouse)
                    if not mouse.buildat == [0, 0]:
                        sounds["action"].play()
                        newobj = objects.object(mouse.buildat - Vector2(4, 4), tileselect[tile] + "-" + tile_rotation)
                        if tileselect[tile] == "antivirus":
                            turrents.add(newobj)
                        gameobjects.add(newobj)
                        oldpos = mouse.pos
                        mouse.pos = Vector2(newobj.rect.left, newobj.rect.top) - Vector2(64, 17)
                        mouse.rect.center = Vector2(newobj.rect.left, newobj.rect.top) - Vector2(64, 17)
                        oldmask = mouse.mask
                        if not tileselect[tile] == "wall":
                            tiles.update("typeobject", mouse)
                        mouse.pos = oldpos
                        mouse.mask = oldmask
                        mouse.buildat = [0, 0]
                        click = 0
            elif pygame.mouse.get_pressed()[2] == 1:
                if click == 0:
                    click = 1
                    sounds["action"].play()
            elif event.button == 4 and click == 1:
                tile += 1
                if tile > len(tileselect) - 1:
                    tile = 0
                settile()
                sounds["action"].play()
            elif event.button == 5 and click == 1:
                tile -= 1
                if tile < 0:
                    tile = len(tileselect) - 1
                settile()
                sounds["action"].play()
        if event.type == pygame.USEREVENT:
            viruses.update(tiles, router, bullets)
            bullets.update()
        if event.type == pygame.USEREVENT+1 and virusescreated < virusestocreate and wavestarted:
            createvirus()
            virusescreated += 1

    window.fill([55, 55, 55])
    ui.text("BITCOIN - " + str(bitcoin), [5, 0], window)
    ui.text("ROUTER HEALTH - " + str(router.health), [5, 40], window)
    ui.fontSize(12)
    if wavestarted:
        ui.text("WAVE " + str(wave) + " - " + str(len(viruses.sprites())) + " ENEMIES LEFT", [5, 80], window)
    else:
        ui.text("WAVE " + str(wave), [5, 80], window)
    ui.fontSize(18)

    tiles.draw(window)
    bullets.draw(window)
    gameobjects.draw(window)
    lines.draw(window)
    router.draw(window)
    viruses.draw(window)
    gamebuttons.draw(window)

    gameobjects.update(bullets)
    gamebuttons.update(mouse)

    if virusestocreate <= virusescreated and len(viruses.sprites()) == 0:
        wavestarted = False
        wavebutton.text = "START WAVE " + str(wave+1)
        virusescreated = 0
        virusestocreate = 0

    if click == 1:
        window.blit(currenttile, mouse.buildat - currentrectpos)

    pygame.display.flip()
pygame.quit()