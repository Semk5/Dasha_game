import pygame
import random
import sys
import os

FPS = 60

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    if colorkey:
        if colorkey == -1:
            image.set_colorkey(image.get_at((0, 0)))
        else:
            image.set_colorkey(colorkey)
        image.convert()
    else:
        image.convert_alpha()
    return image
