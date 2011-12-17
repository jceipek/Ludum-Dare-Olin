#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import os
import pygame
from globals import *
from pygame.locals import *
from Box2D import *
from manager import *

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

def box2d_example():
    world = b2AABB()
    world.lowerBound = (-100, -100)
    world.upperBound = (100, 100)
    gravity = (0, -10)
    doSleep = True
    world = b2World(world, gravity, doSleep)

    groundBodyDef = b2BodyDef()
    groundBodyDef.position = (0, -10)
    groundBody = world.CreateBody(groundBodyDef)
    groundShapeDef = b2PolygonDef()
    groundShapeDef.SetAsBox(50, 10)
    groundBody.CreateShape(groundShapeDef)

    bodyDef = b2BodyDef()
    bodyDef.position = (0, 4)
    body = world.CreateBody(bodyDef)

    shapeDef = b2PolygonDef()
    shapeDef.SetAsBox(1, 1)
    shapeDef.density = 1
    shapeDef.friction = 0.3
    body.CreateShape(shapeDef)
    body.SetMassFromShapes()

    timestep = 1.0 / 60.0
    velocityIterations = 10
    positionIterations = 8

    for i in range(60):
        world.Step(timestep, velocityIterations, positionIterations)
        print body.position, body.angle

    world.gravity = (0, 10)
    for i in range(60):
        world.Step(timestep, velocityIterations, positionIterations)
        print body.position, body.angle
    return 0

class Spaceman(object):
    def __init__(self, body, obj, background):
        self.body = body
        self.obj = obj
        self.sprWalkR = pygame.image.load(os.path.join('astronaut','walking.png'))
        self.sprWalkR.convert()
        self.sprWalkL = pygame.transform.flip(self.sprWalkR, True, False)
        self.obj.blit(background, (0, 0))
        self.obj.blit(self.sprWalkR, (0, 0))
        self.IMG_COUNT = 30
        self.IMG_W = 80

        self.curVel = None
    def getPosition(self):
        return ( (10 - self.body.position.x) * (640/10) + 640/20, (10 - self.body.position.y) * (480/10) + 480/20 )
    def updateImg(self, background, loopcount):
        print self.body.GetLinearVelocity().x
        if abs(self.body.GetLinearVelocity().x) >= 1:
            self.obj.blit(background, (0, 0))
            if self.body.GetLinearVelocity().x > 0: #Moving Left
                self.obj.blit(self.sprWalkL, (-self.IMG_W * (self.IMG_COUNT - loopcount % self.IMG_COUNT - 1), 0))
            else:
                self.obj.blit(self.sprWalkR, (-self.IMG_W * (loopcount % self.IMG_COUNT), 0))
    def motionCheck(self):
        self.curVel = self.body.GetLinearVelocity

        if 0.2 < abs(self.curVel.x) < 1:
            #Try to slow body to stop with impulse
            self.body.ApplyForce(b2Vec2(-(self.body.GetMass()*self.body.GetLinearVelocity().x*FPS/2),0),self.body.GetWorldCenter())
            print "You're too slow!"
    
    def tryMove(x, y):
        #if self.curVel.x < 



def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    w = World(Vect(SCREEN_REAL_WIDTH, SCREEN_REAL_HEIGHT, "meters"), Vect(SCREEN_PIXEL_WIDTH, SCREEN_PIXEL_HEIGHT, "pixels"), GRAVITY)
    groundBodyDef = b2BodyDef()
    groundBodyDef.position = (5, 1)
    groundBody = w.CreateBody(groundBodyDef)
    groundShapeDef = b2PolygonDef()
    groundShapeDef.SetAsBox(5.0, 0.5)
    groundBody.CreateShape(groundShapeDef)

    ground = pygame.Surface((640, 480/10))
    ground = ground.convert()
    ground.fill((255, 255, 255))
    screen.blit(ground, (0, 480 - 480/10))
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

    spaceman = Spaceman(body, obj, background)


    loopcount = 0
    while True:
        loopcount += 1
        tstep = clock.tick(30)

        spaceman.motionCheck()

        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 480 - 480/10))

        w.Step(tstep / 1000.0, 10, 8)
        #print body.position
        posx, posy = spaceman.getPosition()
        #posx = (10 - body.position.x) * (640/10) + 640/20
        #posy = (10 - body.position.y) * (480/10) + 480/20
        #obj.blit(background, (0, 0))
        spaceman.updateImg(background, loopcount)
        #obj.blit(spaceman.spritesheet, (-IMG_W * (loopcount % IMG_COUNT), 0))
        #print posx,posy
        screen.blit(obj, (posx, posy))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_RIGHT:
                    spaceman.tryMove(-20,0)
                if event.key == K_LEFT:
                    body.ApplyForce(b2Vec2(20,0),body.GetWorldCenter())
                if event.key == K_UP:
                    body.ApplyForce(b2Vec2(0,100),body.GetWorldCenter())

        pygame.display.flip()
    return 0

if __name__ == '__main__':
    sys.exit(main())
