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

        return cls._instance

    def convertPixelsToPhysicalCoords(pixelCoords):
        physX = (pixelCoords[0]+self.pixelVect.x)/PIXELS_PER_METER
        physY = (SCREEN_PIXEL_HEIGHT-pixelCoords[1]-self.pixelVect.y)/PIXELS_PER_METER
        return dimension.Vect(physX,physY)
    '''
    def convertPhysicalToPixelCoords(physicalCoords):
        pixX = (physicalCoords[0]'''