#!/usr/bin/python

import cv
import pygame
import sys
import os
from time import time, sleep
import subprocess

#
# Initialize CV
#
C = dict()

C["cam"] = cv.CaptureFromCAM(0)
def next_pg_image():
    cam = C["cam"]
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
size = width, height = 1024, 600
screen = pygame.display.set_mode(size, pygame.FULLSCREEN)

# load image files

top = sys.argv[1] if sys.argv[1:] else "."

image_files = ["%s/%s" % (top,f) for f in os.listdir(top) if f.endswith(".png")]
image_files.extend("%s/%s" % (top, f) for f in os.listdir(top) if f.endswith(".jpg"))
image_files.sort()

if not image_files:
  print "ERROR: no background files found."
  sys.exit(0)

# load the card

card_width = int(height / 300.0 * 215.)
card_height = height

def load_card(i=0):
  card_surf  = pygame.Surface((card_width, card_height))
  card_image = pygame.image.load(image_files[i])
  card_surf.blit(pygame.transform.smoothscale(
      card_image, (card_width, card_height)), (0,0))
  return card_surf

image_idx = 0
card_surf = load_card(image_idx)

# the window in the capture frame
capture_width_crop = 640
capture_height_crop = 400 

# rescaling if necessary
face_width = card_width - 30 
face_height = int(float(face_width) / capture_width_crop * capture_height_crop)
face_surf  = pygame.Surface((face_width, face_height))
# face_surf.set_alpha(255)

# Merged face + card
merge_surf = pygame.Surface((card_width, card_height))

def printer_ready():
  output = subprocess.check_output(["lpq"])
  if "no entries" in output:
    return True
  else:
    return False

def print_image(capture):
  try:
    t = str(time())
    filename = "output/%s.png" % t
    facename = "output/face-%s.png" % t
    pygame.image.save(capture, facename)
    pygame.image.save(merge_surf, filename)
    print "image saved:", filename
    if printer_ready():
      del C["cam"]
      print ">>>>>>> printer"
      subprocess.call(["/usr/bin/lp", "-o", "scaling=60", filename])
      sleep(10.0)
      C["cam"] = cv.CaptureFromCAM(0)
    else:
      print "printer not ready"
  except Exception, e:
    print e


_quit = False
_merge = True

capture = next_pg_image()
while True:
    for e in pygame.event.get():
        if e.type is pygame.QUIT:
            _quit = True
        if e.type is pygame.KEYDOWN:

          if e.key == pygame.K_ESCAPE:
            _quit = True

          elif e.key == pygame.K_SPACE:
            _merge = not _merge

          elif e.key == pygame.K_PAGEDOWN:
            print_image(capture)

          elif e.key == pygame.K_LEFT:
            image_idx = (image_idx - 1) % len(image_files)
            card_surf = load_card(image_idx)

          else:
            image_idx = (image_idx + 1) % len(image_files)
            card_surf = load_card(image_idx)


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

    if _merge:
      center(merge_surf, face_surf, None, card_height - face_height - 10)

    screen.fill((255, 255, 255))
    center(screen, merge_surf)

    pygame.display.flip()



subprocess.call(["lprm", "-"])
pygame.display.quit()
del C["cam"]
