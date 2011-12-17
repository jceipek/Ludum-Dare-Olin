#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import os
import pygame
from pygame.locals import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    IMG_COUNT = 30
    IMG_W = 80
    IMG_H = 80
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))
    
    walker = pygame.Surface((IMG_W, IMG_H))
    walker.convert()
    walker.fill((255, 0, 0))
    spritesheet = pygame.image.load(os.path.join('astronaut','walking.png'))
    spritesheet.convert()
    loopcount = 0
    while True:
        loopcount += 1
        tstep = clock.tick(30)
        screen.blit(background, (0, 0))
        walker.blit(background, (0, 0))
        walker.blit(spritesheet, (-IMG_W * (loopcount % IMG_COUNT), 0))
        screen.blit(walker, (int(loopcount * (38.0/30.0)), 400))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
    return 0

if __name__ == '__main__':
    sys.exit(main())
