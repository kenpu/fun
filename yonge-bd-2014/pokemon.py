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

def center(surf0, surf1, x=None, y=None):
    rect0 = surf0.get_rect()
    rect1 = surf1.get_rect()
    if x == None:
        x = rect0[2]/2-rect1[2]/2
    if y == None:
        y = rect0[3]/2-rect1[3]/2
    surf0.blit(surf1, (x,y))

#
# Initialize PyGame display
#
pygame.init()
size = width, height = 1366, 744
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

_quit = False

# load the card
card_width = int(height / 300.0 * 215.)
card_height = height
card_surf  = pygame.Surface((card_width, card_height))
card_image = pygame.image.load("card0.jpg")
card_surf.blit(pygame.transform.smoothscale(
    card_image, (card_width, card_height)), (0,0))


# the window in the capture frame
capture_width_crop = 640
capture_height_crop = 400 

# rescaling if necessary
face_width = card_width - 30 
face_height = int(float(face_width) / capture_width_crop * capture_height_crop)
face_surf  = pygame.Surface((face_width, face_height))
# face_surf.set_alpha(255)

# build a head mask
mask_surf = pygame.Surface((face_width, face_height))
pygame.draw.ellipse(mask_surf, 
    (0,0,0), (0, 0, face_width, face_height))
mask = pygame.mask.from_surface(mask_surf)

# Merged face + card
merge_surf = pygame.Surface((card_width, card_height))

while True:
    for e in pygame.event.get():
        if e.type is pygame.QUIT:
            _quit = True
        if e.type is pygame.KEYDOWN:
            _quit = True

    if _quit: break

    capture = next_pg_image()
    rect = capture.get_rect()

    # update face_surf
    w, h = rect[2], rect[3]
    face_surf.blit(
        pygame.transform.smoothscale(
            capture.subsurface(
                w/2 - capture_width_crop/2,
                h/2 - capture_height_crop/2,
                capture_width_crop,
                capture_height_crop), (face_width, face_height)), (0,0))

    # update the card_background
    merge_surf.fill((255,255,255))
    center(merge_surf, card_surf)
    center(merge_surf, face_surf, None, 
        card_height - face_height - 10)

    screen.fill((255, 255, 255))
    center(screen, merge_surf)

    pygame.display.flip()

pygame.image.save(merge_surf, "surf0.png")

pygame.display.quit()
del cam
