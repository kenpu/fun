import pygame
import cv
import sys

pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

def get_image(cam):
    cv_im = cv.QueryFrame(cam)
    depth = cv_im.depth
    (r, g, b) = [cv.CreateImage(size, depth, 1) for i in range(3)]
    cv.Split(cv_im, b, g, r, None)
    cv.Merge(r, g, b, None, cv_im)
    return pygame.image.frombuffer(cv_im.tostring(), cv.GetSize(cv_im), "RGB")


cam = cv.CaptureFromCAM(0)
_quit = False
surface = pygame.Surface(size)

while not _quit:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            _quit = True
        if e.type is pygame.KEYDOWN:
            _quit = True

    if _quit:
        break

    im = get_image(cam)
    rect = im.get_rect()

    # update the surface
    surface.blit(im, rect)

    # draw a box
    pygame.draw.rect(surface,
        (255, 0, 0),
        (100, 100, 100, 100),
        5)


    screen.fill((0,0,0))
    screen.blit(surface, (0,0, 200, 200))

    pygame.display.flip()

pygame.display.quit()
del cam
