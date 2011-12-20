import pygame
import os

IMAGES_TO_LOAD = {"crate"         :("","glowcrate.png"),
                  "door"          :("","door.png"),
                  "floorTurret"   :("","floorTurret.png"),
                  "laserBottom"   :("","laserBottom.png"),
                  "laserTop"      :("","laserTop.png"),
                  "newcrate"      :("","newcrate.png"),
                  "simplePlatform":("","simplePlatform.png"),
                  "simpleWall"    :("","simpleWall.png"),
                  "turret"        :("","turret.png"),
                  "walkingRight"  :("astronaut", "walkingRight.png"),
                  "walkingLeft"   :("astronaut", "walkingLeft.png"),
                  "jumpingRight"  :("astronaut", "jumpingRight.png"),
                  "jumpingLeft"   :("astronaut", "jumpingLeft.png"),
                  "standingRight" :("astronaut", "standingRight.png"),
                  "standingLeft" :("astronaut", "standingLeft.png"),
                  "roombg"        :("","roombg.png")
                  }

class ImageHandler(dict):
    #implement a singleton pattern here...
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ImageHandler,cls).__new__(cls,*args,**kwargs)
            self = cls._instance
            for name in IMAGES_TO_LOAD.keys():
                folder = IMAGES_TO_LOAD[name][0]
                file = IMAGES_TO_LOAD[name][1]
                img = pygame.image.load(os.path.join(folder, file))
                img = img.convert_alpha()
                self[name] = img

        return cls._instance



# TESTING CODE BELOW
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
