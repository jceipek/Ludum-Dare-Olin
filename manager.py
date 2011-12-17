#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import pygame
from pygame.locals import *
from Box2D import *

class Body(object):
    pass

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
    def __init__(self, size_pixels, size_meters, gravity):
        self.size_pixels = size_pixels
        self.size_meters = size_meters
        self.ppm = Vect(size_pixels.x / size_meters.x, 
                        size_pixels.y / size_meters.y, "p/m")
        self.bodies = []
        world = b2AABB()
        world.lowerBound = (0, 0)
        world.upperBound = (self.size_meters.x, self.size_meters.y)
        doSleep = True
        super(World, self).__init__(world, gravity, doSleep)

    def ToMeters(self, vect):
        return Vect()

def main():
    return 0

if __name__ == '__main__':
    sys.exit(main())
