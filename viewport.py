from __future__ import division

import pygame
from globals import *
from dimension import Vect

class Viewport(object):
    # here we haz a singletonion patterner
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Viewport,cls).__new__(cls,*args,**kwargs)
            self = cls._instance
            self.pixelVect = Vect(0,0)
            self.levelHeight = None
            self.hasMoved = False

        return cls._instance

    def convertPixelsToPhysicalCoords(self,pixelCoords):
        physX = (pixelCoords[0] + self.pixelVect.x) / PIXELS_PER_METER
        physY = (PIXELS_PER_METER * self.levelHeight - pixelCoords[1] - self.pixelVect.y) / PIXELS_PER_METER 
        return Vect(physX,physY)
    
    def convertPhysicalToPixelCoords(self,physicalCoords):
        pixX = physicalCoords[0]*PIXELS_PER_METER - self.pixelVect.x
        pixY = PIXELS_PER_METER * self.levelHeight - self.pixelVect.y - physicalCoords[1] * PIXELS_PER_METER
        return Vect(int(pixX),int(pixY))

    def move(self,vect):
        self.pixelVect += vect
        self.hasMoved = True

if __name__ == "__main__":
    vp = Viewport()
    vp.levelHeight = 60
    vp.pixelVect += Vect(30*PIXELS_PER_METER,30*PIXELS_PER_METER)
    test = Vect(30,30)
    a = vp.convertPhysicalToPixelCoords(test)
    test2 = vp.convertPixelsToPhysicalCoords(a)
    print "Test: ",test
    print "a:    ",a
    print "Test2:",test2