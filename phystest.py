#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import os
import pygame
from globals import *
from pygame.locals import *
from Box2D import *
import manager as mgr
import room as rm
import dimension as dim

#class myContactListener(b2ContactListener):
#    def __init__(self):
#        b2ContactListener.__init__(self)
#    def BeginContact(self, contact):
#        pass
#    def EndContact(self, contact):
#        pass
#    def PreSolve(self, contact, oldManifold):
#        pass
#    def PostSolve(self, contact, impulse):
#        pass


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen_width = dim.Dimension(value=SCREEN_REAL_WIDTH, units={'m': 1})
    screen_height = dim.Dimension(value=SCREEN_REAL_HEIGHT, units={'m': 1})
    w = mgr.World(dim.Vect(screen_width, screen_height), GRAVITY)

    room = rm.Room(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)
    room.platforms.append(rm.StaticPlatform(w, dim.Vect(8.0 * METER, 3.0 * METER), dim.Vect(8.0*METER,1.0*METER)))

    spaceman = rm.Spaceman(w, dim.Vect(9.0 * METER, 9.0 * METER))
    spaceman.add()

    for object in room.GetAllObjects():
        object.add()


    loopcount = 0
    while True:
        loopcount += 1
        tstep = clock.tick(30)

        spaceman.motionCheck()

        screen.blit(background, (0, 0))

        w.Step(tstep / 1000.0, 10, 8)

        spaceman.updateImg(background, loopcount)
        spaceman.blitToScreen(screen)

        for object in room.GetAllObjects():
            object.blitToScreen(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_UP:
                    spaceman.body.ApplyForce(b2Vec2(0,100),spaceman.body.GetWorldCenter())
                if event.key == K_g:
                    w.gravity=(0,0)
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_RIGHT]:
            spaceman.tryMove(10, 0)
        if keysPressed[K_LEFT]:
            spaceman.tryMove(-10,0)

        pygame.display.flip()
    return 0

if __name__ == '__main__':
    sys.exit(main())
