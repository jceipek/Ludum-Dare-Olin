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
    screen = pygame.display.set_mode((SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT))

    room = rm.Room(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)
    #room.boxes.append(rm.Box((5,5)))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    screen_width = mgr.Dimension(value=SCREEN_REAL_WIDTH, units={'m': 1})
    screen_height = mgr.Dimension(value=SCREEN_REAL_HEIGHT, units={'m': 1})
    w = w = mgr.World(mgr.Vect(screen_width, screen_height), GRAVITY)
    groundBodyDef = b2BodyDef()
    groundBodyDef.position = (5, 1)
    groundBody = w.CreateBody(groundBodyDef)
    groundShapeDef = b2PolygonDef()
    groundShapeDef.SetAsBox(5.0, 0.5)
    groundBody.CreateShape(groundShapeDef)

    ground = pygame.Surface((SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT/10))
    ground = ground.convert()
    ground.fill((255, 0, 255))
    screen.blit(ground, (0, SCREEN_PIXEL_HEIGHT - SCREEN_PIXEL_HEIGHT/10))
    pygame.display.flip()

    bodyDef = b2BodyDef()
    bodyDef.position = (5, 10)
    bodyDef.fixedRotation = True
    bodyDef.linearDamping = 0.2
    body = w.CreateBody(bodyDef)
    shapeDef = b2PolygonDef()
    shapeDef.SetAsBox(1, 1)
    shapeDef.density = 0.1
    shapeDef.friction = 0.1
    body.CreateShape(shapeDef)
    body.SetMassFromShapes()

    IMG_COUNT = 30
    IMG_W = 80
    IMG_H = 80
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((255, 255, 255))

    obj = pygame.Surface((IMG_W, IMG_H))
    obj = obj.convert()
    obj.fill((255, 0, 0))

    meter = mgr.Dimension(value=1.0, units={'m': 1})
    spaceman = rm.Spaceman(w, mgr.Vect(9.0 * meter, 9.0 * meter))
    spaceman.add()

    for object in room.GetAllObjects():
        object.add()


    loopcount = 0
    while True:
        loopcount += 1
        tstep = clock.tick(30)

        spaceman.motionCheck()

        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 480 - 480/10))

        w.Step(tstep / 1000.0, 10, 8)
        #posx, posy = spaceman.getPosition()
        #posx = (10 - body.position.x) * (640/10) + 640/20
        #posy = (10 - body.position.y) * (480/10) + 480/20
        #obj.blit(background, (0, 0))
        spaceman.updateImg(background, loopcount)
        #obj.blit(spaceman.spritesheet, (-IMG_W * (loopcount % IMG_COUNT), 0))
        #screen.blit(obj, (posx, posy))

        spaceman.blitToScreen(screen)

        for object in room.GetAllObjects():
            screen.blit(object.obj, object.getPosition())
            print object.getPosition()

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_UP:
                    body.ApplyForce(b2Vec2(0,100),body.GetWorldCenter())
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
