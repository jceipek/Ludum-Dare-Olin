#!/usr/bin/python
# -*- coding: us-ascii -*-

import math
import sys

EPSILON = 0.00001

class Vect(object):
    '''
    A generic vector object
    '''
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect(self.x + other[0], self.y + other[1])

    def __mul__(self, num):
        return Vect(num * self.x, num * self.y)

    def __rmul__(self, num):
        return Vect(self.x * num, self.y * num)

    def __div__(self, other):
        return Vect(self.x / other, self.y / other)

    def __sub__(self, other):
        return Vect(self.x - other[0], self.y - other[1])

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

    #def Norm(self):
    #    return (self.x ** 2 + self.y ** 2) ** fraction(1, 2)

    def __str__(self):
        return '<%s, %s>' % (self.x, self.y)

    def __eq__(self, other):
        return self.x-other[0] <= EPSILON and self.y-other[1] <= EPSILON

    def __ne__(self, other):
        return self.__eq__(other)

def vecttest():
    a = Vect(0, 0)
    b = Vect(0, 0)
    c = Vect(1.0000001, 2.333348)
    d = Vect(1.000000099, 2.333348)
    assert c == d
    assert a == b
    assert b != c
    assert a != d

if __name__ == '__main__':
    sys.exit(vecttest())
