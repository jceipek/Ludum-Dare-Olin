#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import pygame
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

class World(b2World):
    def __init__(self, size, gravity):
        self.size = size # [m]
        self.bodies = []
        world = b2AABB()
        world.lowerBound = (0, 0)
        world.upperBound = (self.size.x, self.size.y)
        doSleep = True
        super(World, self).__init__(world, gravity, doSleep)

    def ToMeters(self, vect):
        return Vect()

class Rect(Box2D.b2Body):
    def __init__(self, world, pos):
        bodyDef = b2BodyDef()
        bodyDef.position = pos
        self = world.CreateBody(bodyDef)

def main():
    w = World(Vect(10, 10, "meters"), (0, -10))
    r = Rect(w, (5, 5))
    print r
    return 0

if __name__ == '__main__':
    sys.exit(main())
