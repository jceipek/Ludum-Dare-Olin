import pygame
import os

IMAGES_TO_LOAD = ("crate.png",
                  "door.png",
                  "floorTurret.png",
                  "laserBottom.png",
                  "laserTop.png",
                  "newcrate.png",
                  "simplePlatform.png",
                  "turret.png")

class ImageHandler(dict):
    #implement a singleton pattern here...
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageHandler,cls).__new__(cls,*args,**kwargs)

        return cls._instance

    def __init__(self):
        for name in IMAGES_TO_LOAD:
            img = pygame.image.load(os.path.join(name))
            img = img.convert()
            self[name] = img


if __name__ == "__main__":

    from globals import *
    from pygame.locals import *
    pygame.init()
    surface = pygame.display.set_mode((SCREEN_PIXEL_WIDTH,SCREEN_PIXEL_HEIGHT))
    ImageHandler()

    cont = True
    while cont:
        for event in pygame.event.get():
                if event.type == QUIT:
                    cont = False
