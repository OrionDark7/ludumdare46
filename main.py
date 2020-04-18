import pygame
from pygame.math import Vector2
from game import map, objects

pygame.init()

window = pygame.display.set_mode([1280, 720])
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
    def position(self):
        self.rect.left, self.rect.top = pygame.mouse.get_pos()
        self.pos  = pygame.mouse.get_pos()

tiles = map.createmap()
computers = pygame.sprite.Group()
currenttile = pygame.image.load("./resources/images/computer.png")
currenttile.set_alpha(128)
currenttilerect = currenttile.get_rect()
currentrectpos = Vector2(currenttilerect.width/2, currenttilerect.height/2)

mouse = Mouse()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            mouse.position()
            if click == 1:
                tiles.update("click", computers, mouse)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse.position()
            if click == 0:
                click = 1
            elif click == 1:
                click = 2
            if click == 2:
                tiles.update("click", computers, mouse)
                if not mouse.buildat == [0,0]:
                    computers.add(objects.computer(mouse.buildat))
                    mouse.buildat = [0,0]
                    click = 0

    print(mouse.buildat, currentrectpos)

    tiles.draw(window)
    computers.draw(window)
    print(computers)
    if click == 1:
        window.blit(currenttile, mouse.buildat - currentrectpos)

    pygame.display.flip()
pygame.quit()