#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import os
import math
import pygame
from globals import *
from pygame.locals import *
from Box2D import *
import manager as mgr
import room as rm
import dimension as dim

class myContactListener(b2ContactListener):
    """
    Handles all of the contact states passed in from Box2D.

    """
    test = []
    def __init__(self):
        super(myContactListener, self).__init__()

    def handleCall(self, state, point):
        #print state
        if not self.test: return

        cp          = myContactPoint()
        cp.shape1   = point.shape1
        cp.shape2   = point.shape2
        cp.position = point.position.copy()
        cp.normal   = point.normal.copy()
        cp.id       = point.id
        cp.state    = state
        self.test.points.append(cp)
        return cp

    def Add(self, point):
        cp = self.handleCall(myContactTypes.contactAdded, point)
        if cp.shape1.GetBody().GetUserData()=="spaceman" and cp.shape2.GetBody().GetUserData()=="staticPlatform" \
        or cp.shape2.GetBody().GetUserData()=="spaceman" and cp.shape1.GetBody().GetUserData()=="staticPlatform" :
            spaceman.touchingGround += 1

    def Persist(self, point):
        self.handleCall(myContactTypes.contactPersisted, point)

    def Remove(self, point):
        cp = self.handleCall(myContactTypes.contactRemoved, point)
        if cp.shape1.GetBody().GetUserData()=="spaceman" and cp.shape2.GetBody().GetUserData()=="staticPlatform" \
        or cp.shape2.GetBody().GetUserData()=="spaceman" and cp.shape1.GetBody().GetUserData()=="staticPlatform" :
            spaceman.touchingGround -= 1

class myContactPoint:
    """
    Structure holding the necessary information for a contact point.
    All of the information is copied from the contact listener callbacks.
    """
    shape1 = None
    shape2 = None
    normal = None
    position = None
    velocity = None
    id  = None
    state = 0

class myContactTypes:
    """
    Acts as an enum, holding the types necessary for contacts:
    Added, persisted, and removed
    """
    contactUnknown = 0
    contactAdded = 1
    contactPersisted = 2
    contactRemoved = 3

def kickMagnitude(tminus):
    t = float(FRAMERATE - tminus) / float(FRAMERATE)
    a = 2.0
    b = 0.5
    c = 0.33
    return math.exp(-((t - b)**2) / (2 * c**2))

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
    w.listener = myContactListener() #I hate bugs. 
    w.SetContactListener(w.listener)
    w.listener.test = w

    room = rm.Room(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT)
    groundPos = dim.Vect(SCREEN_REAL_WIDTH * METER / 2, 3.0 * METER)
    groundSize = dim.Vect(SCREEN_REAL_WIDTH * METER, 1.0 * METER)
    ground = rm.StaticPlatform(w, groundPos, groundSize)
    room.platforms.append(ground)

    global spaceman
    spaceman = rm.Spaceman(w, dim.Vect(9.0 * METER, 9.0 * METER))
    room.spawnPoints.append(spaceman)

    for object in room.GetAllObjects():
        object.add()


    loopcount = 0
    kickcount = 0
    while True:
        loopcount += 1
        tstep = clock.tick(FRAMERATE)
        w.points=[]

        spaceman.motionCheck()

        screen.blit(background, (0, 0))

        w.Step(tstep / 1000.0, 10, 8)

        spaceman.updateImg(background, loopcount)
        
        for object in room.GetAllObjects():
            object.blitToScreen(screen)

        body_pairs = [(p.shape1.GetBody(), p.shape2.GetBody()) for p in w.points]
        print 'start'
        for body1, body2 in body_pairs:
            print body1.GetUserData(), body2.GetUserData()
        print 'end'

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_UP:
                    if spaceman.touchingGround >= 1:
                        spaceman.body.ApplyForce(b2Vec2(0,500),
                                                 spaceman.body.GetWorldCenter())
                if event.key == pygame.K_j:
                    if kickcount <= 0:
                        kickcount = 1.0 * FRAMERATE
                        kickd = dim.Vect(-1 * METER, 0 * METER) * 3
                if event.key == pygame.K_k:
                    if kickcount <= 0:
                        kickcount = 1.0 * FRAMERATE
                        kickd = dim.Vect(0 * METER, 1 * METER) * 15
                if event.key == pygame.K_l:
                    if kickcount <= 0:
                        kickcount = 1.0 * FRAMERATE
                        kickd = dim.Vect(1 * METER, 0 * METER) * 3
                if event.key == pygame.K_i:
                    if kickcount <= 0:
                        kickcount = 1.0 * FRAMERATE
                        kickd = dim.Vect(0 * METER, -1 * METER) * 15
        keysPressed = pygame.key.get_pressed()
        if keysPressed[K_RIGHT]:
            spaceman.tryMove(10, 0)
        if keysPressed[K_LEFT]:
            spaceman.tryMove(-10,0)

        if kickcount > 1:
            kick = kickd * kickMagnitude(kickcount)
            gravity = dim.Vect(0 * METER, -10 * METER) + kick
            # print gravity
            w.gravity = gravity.Strip()
            kickcount -= 1
            for obj in room.GetAllObjects():
                obj.body.WakeUp()
        elif kickcount > 0:
            w.gravity = GRAVITY
            kickcount -= 1

        pygame.display.flip()
    return 0

if __name__ == '__main__':
    sys.exit(main())
