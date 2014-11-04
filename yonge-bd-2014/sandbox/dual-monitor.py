import cv
import pygame
import sys

#
# Initialize CV
#
cam = cv.CaptureFromCAM(0)
def next_pg_image():
    cv_im = cv.QueryFrame(cam)
    depth = cv_im.depth
    s = cv.GetSize(cv_im)
    (r,g,b) = [cv.CreateImage(s, depth, 1) for i in range(3)]
    cv.Split(cv_im, b, g, r, None)
    cv.Merge(r, g, b, None, cv_im)
    return pygame.image.frombuffer(cv_im.tostring(), s, 'RGB')


#
# Initialize PyGame display
#
pygame.init()
size = width, height = 640, 480
screen = pygame.display.set_mode(size)

_quit = False
surf0 = pygame.Surface(size)
surf1 = pygame.Surface((width/2, height))
surf2 = pygame.Surface((width/2, height))

while True:
    for e in pygame.event.get():
        if e.type is pygame.QUIT:
            _quit = True
        if e.type is pygame.KEYDOWN:
            _quit = True

    if _quit: break

    im = next_pg_image()
    rect = im.get_rect()

    # update surf1
    surf1.blit(im.subsurface((width/2,0, width/2, height)), (0,0))

    # update suf2
    surf2.blit(im.subsurface((0, 0, width/2, height)), (0,0))

    # update surf0
    surf0.blit(pygame.transform.scale(surf1, (100, 200)), (0,0))
    surf0.blit(surf2, (width/2,0))

    screen.fill((0,0,0))
    screen.blit(surf0, (0, 0))

    pygame.display.flip()

pygame.display.quit()
del cam
