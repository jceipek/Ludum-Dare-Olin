#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import pygame
from pygame.locals import *
from Box2D import *
import manager

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

    w = World(Vect(10, 10, "meters"), Vect(640, 480, "pixels"), (0, -10))
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
    body = w.CreateBody(bodyDef)
    shapeDef = b2PolygonDef()
    shapeDef.SetAsBox(1, 1)
    shapeDef.density = 1
    shapeDef.friction = 0.3
    body.CreateShape(shapeDef)
    body.SetMassFromShapes()

    obj = pygame.Surface((640/10, 480/10))
    obj = obj.convert()
    obj.fill((0, 255, 0))

    while True:
        tstep = clock.tick(30)
        screen.blit(background, (0, 0))
        screen.blit(ground, (0, 480 - 480/10))

        w.Step(tstep / 1000.0, 10, 8)
        print body.position
        pos = (10 - body.position.y) * (480/10) + 480/20
        screen.blit(obj, (320, pos))

        for event in pygame.event.get():
            if event.type == QUIT:
                return

        pygame.display.flip()
    return 0

if __name__ == '__main__':
    sys.exit(main())
