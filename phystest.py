#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import os
import pygame
from globals import *
from pygame.locals import *
from Box2D import *
from manager import *

class myContactListener(b2ContactListener):
    def __init__(self):
        b2ContactListener.__init__(self)
    def BeginContact(self, contact):
        pass
    def EndContact(self, contact):
        pass
    def PreSolve(self, contact, oldManifold):
        pass
    def PostSolve(self, contact, impulse):
        pass

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    w = World(Vect(GAME_REAL_WIDTH, GAME_REAL_HEIGHT, "meters"), Vect(GAME_PIXEL_WIDTH, GAME_PIXEL_HEIGHT, "pixels"), GRAVITY)
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
    body = w.CreateBody(bodyDef)
    shapeDef = b2PolygonDef()
    shapeDef.SetAsBox(1, 1)
    shapeDef.density = 0.1
    shapeDef.friction = 0
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
    spritesheet = pygame.image.load(os.path.join('astronaut','walking.png'))
    spritesheet.convert()
    loopcount = 0

    #For Testing
    #inAir = True

    while True:
        loopcount += 1
        tstep = clock.tick(30)
        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 480 - 480/10))

        w.Step(tstep / 1000.0, 10, 8)
        print body.position
        posx = (10 - body.position.x) * (640/10) + 640/20
        posy = (10 - body.position.y) * (480/10) + 480/20
        obj.blit(background, (0, 0))
        obj.blit(spritesheet, (-IMG_W * (loopcount % IMG_COUNT), 0))
        print posx,posy
        screen.blit(obj, (posx, posy))

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    return
                if event.key == K_RIGHT:
                    body.ApplyForce(b2Vec2(-20,0),groundBody.GetWorldCenter())
                if event.key == K_LEFT:
                    body.ApplyForce(b2Vec2(20,0),groundBody.GetWorldCenter())
                if event.key == K_UP:
                    body.ApplyForce(b2Vec2(0,100), groundBody.GetWorldCenter())

        pygame.display.flip()
    return 0

if __name__ == '__main__':
    sys.exit(main())
