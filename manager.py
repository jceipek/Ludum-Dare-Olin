#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import pygame
import math
from pygame.locals import *
from Box2D import *

from globals import *

class Vect(object):
    def __init__(self, x, y, units):
        self.x = x
        self.y = y
        self.units = units

    def __add__(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible units")
        return Vect(self.x + other.x, self.y + other.y, self.units)

    def meters(self):
        if units = "meters":
            return self
        else:
            x = self.x / PIXELS_PER_METER
            y = (768 - self.y) / PIXELS_PER_METER
            return Vect(x, y, "meters")

    def pixels(self):
        if units = "pixels":
            return self
        else:
            x = self.x * PIXELS_PER_METER
            y = SCREEN_PIXEL_SIZE - (self.y * PIXELS_PER_METER)
            return Vect(x, y, "pixels")

class World(b2World):
    def __init__(self, size, gravity):
        self.size = size # [m]
        self.bodies = []
        world = b2AABB()
        world.lowerBound = (0, 0)
        world.upperBound = (self.size.x, self.size.y)
        doSleep = True
        super(World, self).__init__(world, gravity, doSleep)

class Rect(object):
    def __init__(self, world, pos, size, density):
        bodyDef = b2BodyDef
        bodyDef.position = (pos.meters().x, pos.meters().y)
        self.body = world.CreateBody(bodyDef)

        shapeDef = b2PolygonDef()
        shapeDef.SetAsBox(size.meters().x / 2.0, size.meters.y / 2.0)
        shapeDef.density = density
        shapeDef.linearDamping = AIR_RESISTANCE
        shapeDef.friction = FRICTION
        
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShape()

    def GetCornersPixels(self):
        

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))

    screen.blit(background, (0, 0))

    clock = pygame.time.Clock()

    w = World(Vect(SCREEN_REAL_WIDTH, SCREEN_REAL_HEIGHT, "meters"), GRAVITY)
    groundRectPos = Vect(SCREEN_REAL_WIDTH / 2.0, 0.5, "meters")
    groundRectSize = Vect(SCREEN_REAL_WIDTH, 1.0, "meters")
    groundRect = Rect(w, groundRectPos, groundRectSize, 0)



if __name__ == '__main__':
    sys.exit(main())
