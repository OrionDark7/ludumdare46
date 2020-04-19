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
        self.listmap = []
        self.profit = 0
        self.waveend = True
        self.justwaveend = False
        self.dontrepair = False
    def position(self):
        self.rect.left, self.rect.top = pygame.mouse.get_pos()
        self.pos = pygame.mouse.get_pos()

mouse = Mouse()

tiles, lines, mouse.listmap = map.createmap()
gameobjects = pygame.sprite.Group()
turrents = pygame.sprite.Group()
bullets = pygame.sprite.Group()
viruses = pygame.sprite.Group()
effects = pygame.sprite.Group()
gamebuttons = pygame.sprite.Group()
wavebutton = ui.button("START WAVE 1", [5, 670])
shopbutton = ui.button("SHOP", [5, 620])
gamebuttons.add(wavebutton)
gamebuttons.add(shopbutton)
tileselect = ["computer", "firewall", "antivirus", "server", "repair"]
tileprice = [5, 10, 20, 60, 10]
tile = 0
bitcoin = 1000
wave = 0
wavestarted = False
tile_rotation = "left"
currenttile = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
currenttile_ = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
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
    global tile, tileselect, currenttile, currenttilerect, currentrectpos, tile_rotation, currenttile_
    currenttile = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
    currenttile_ = pygame.image.load("./resources/images/" + tileselect[tile] + "-" + tile_rotation + ".png")
    currenttile.set_alpha(128)
    currenttilerect = currenttile.get_rect()
    currentrectpos = Vector2(currenttilerect.width / 2, currenttilerect.height / 2)

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
                if tileselect[tile] == "repair":
                    tiles.update("clickdead", mouse)
                else:
                    tiles.update("click", mouse)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.position()
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
                    pygame.time.set_timer(pygame.USEREVENT + 1, 2000)
                    sounds["action"].play()
                    mouse.waveend = False
                elif shopbutton.click(mouse):
                    if click == 0:
                        click = 1
                        sounds["action"].play()
                        shopbutton.text = "EXIT SHOP"
                    elif shopbutton.text == "EXIT SHOP":
                        click = 0
                        sounds["action"].play()
                        shopbutton.text = "SHOP"
                elif click == 1:
                    click = 2
                    sounds["action"].play()
                if click == 2:
                    tiles.update("click", mouse)
                    if not mouse.buildat == [0, 0] and bitcoin >= tileprice[tile]:
                        sounds["action"].play()
                        if not tileselect[tile] == "repair":
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
                                tiles.update("listmap", mouse)
                        if tileselect[tile] == "repair":
                            oldpos = mouse.pos
                            oldmask = mouse.mask
                            mouse.rect.center = mouse.buildat - Vector2(64, 17)
                            tiles.update("repair", mouse)
                            tiles.update("listmap", mouse)
                            newobj = mouse
                            tiles.update("alive", mouse)
                        mouse.pos = oldpos
                        mouse.mask = oldmask
                        mouse.buildat = [0, 0]
                        mouse.rect.center = oldpos
                        click = 1
                        if not mouse.dontrepair:
                            neweffect = entities.effects(newobj.rect.center, "-"+str(tileprice[tile])+"B", color=[188, 28, 36])
                            effects.add(neweffect)
                            bitcoin -= int(tileprice[tile])
                        mouse.dontrepair = False
                    elif mouse.buildat == [0, 0]:
                        click = 1
                    elif bitcoin < tileprice[tile]:
                        neweffect = entities.effects([656, 610], "NOT ENOUGH MONEY!", color=[188, 28, 36])
                        effects.add(neweffect)
                        click = 1
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
            viruses.update(tiles, router, bullets, effects, mouse)
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
    if wavestarted:
        bullets.draw(window)
    gameobjects.draw(window)
    lines.draw(window)
    router.draw(window)
    viruses.draw(window)
    gamebuttons.draw(window)
    effects.draw(window)

    bitcoin += mouse.profit
    mouse.profit = 0

    gameobjects.update(bullets, effects, mouse)
    gamebuttons.update(mouse)
    effects.update()
    tiles.update("listmap", mouse)
    mouse.justwaveend = False

    if virusestocreate <= virusescreated and len(viruses.sprites()) == 0:
        wavestarted = False
        mouse.waveend = True
        if not mouse.waveend:
            mouse.justwaveend = True
            gameobjects.update(bullets, effects, mouse)
        wavebutton.text = "START WAVE " + str(wave+1)
        virusescreated = 0
        virusestocreate = 0


    if click == 1:
        window.blit(currenttile, mouse.buildat - currentrectpos - Vector2(4, 4))
        window.blit(currenttile_, [640, 620])
        ui.fontSize(18)
        ui.centertext(tileselect[tile].capitalize(), [660, 650], window)
        ui.fontSize(12)
        if bitcoin < tileprice[tile]:
            ui.centertext(str(tileprice[tile]) + " BITCOIN", [660, 680], window, color=[188, 28, 36])
        else:
            ui.centertext(str(tileprice[tile]) + " BITCOIN", [660, 680], window, color=[42, 216, 93])
        ui.fontSize(18)

    pygame.display.flip()
pygame.quit()