import pygame

pygame.init()

window = pygame.display.set_mode([1280, 720])
window.fill([55, 55, 55])

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
pygame.quit()