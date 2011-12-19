#!/usr/bin/python
# -*- coding: us-ascii -*-

import math

class Vect(object):
    '''
    A generic vector object
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vect(other * self.x, other * self.y)

    def __rmul__(self, other):
        return Vect(self.x * other, self.y * other)

    def __div__(self, other):
        return Vect(self.x / other, self.y / other)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def __len__(self):
        return 2
    
    def __getitem__(self, value):
        if value == 0:
            return self.x
        if value == 1:
            return self.y
        raise ValueError, "Index out of bounds for 2D vector: "+str(value)

    def Rotate(self, theta):
        x, y = self.x, self.y
        newx = x * math.cos(theta) - y * math.sin(theta)
        newy = x * math.sin(theta) + y * math.cos(theta)
        self.x = newx
        self.y = newy

    def MirrorH(self):
        return Vect(-self.x, self.y)

    def MirrorV(self):
        return Vect(self.x, -self.y)

    def __str__(self):
        return '<%s, %s>' % (self.x, self.y)
