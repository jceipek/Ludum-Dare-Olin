import pygame
import renderableObjects as ro
from dimension import Vect
from viewport import Viewport
from globals import *

class Level(object):
    '''
    The level loads a level from a file.
    It then initializes all the sprites
    and the appropriate sprite groups.
    '''

    STARS = 0
    ROOM_BG = 1
    FIXED = 2
    DYNAMIC = 3
    EYE_CANDY = 4
    OVERLAY = 5

    def __init__(self,filename):
        self.allObjects = pygame.sprite.LayeredDirty()
        self.physicalSize = Vect(20,10)
        self.drawDebug = False

    def setup(self):
        # Separate setup function such that Level properties
        # such as physical size can be read before RenderableObjects
        # are created
        box = ro.Crate((0,0))
        box.add(self.allObjects)
        box = ro.Crate((0,10))
        box.add(self.allObjects)
        print "Physical position: ",box.physicalPosition
        print "Rect: ",box.rect.center

    def update(self):
        '''
        Handles logic for a game step
        '''
        pass

    def render(self,surface):
        '''
        Renders a game step after the logic is complete
        '''
        self.allObjects.draw(surface)

        if self.drawDebug:
            upperLeftCorner = Viewport().convertPhysicalToPixelCoords((0,self.physicalSize.y))
            size = self.physicalSize * PIXELS_PER_METER
            debugRect = pygame.Rect(upperLeftCorner,size)
            pygame.draw.rect(surface,(255,0,0),debugRect,1)