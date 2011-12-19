import pygame
import renderableObjects as ro
from dimension import Vect
from viewport import Viewport
from globals import *
from images import ImageHandler

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

    def __init__(self,name):
        self.allObjects = pygame.sprite.LayeredDirty()
        bgimage = ImageHandler()[name]
        self.physicalSize = Vect(float(bgimage.get_width())/PIXELS_PER_METER,float(bgimage.get_height())/PIXELS_PER_METER)
        self.drawDebug = False

    def setup(self):
        # Separate setup function such that Level properties
        # such as physical size can be read before RenderableObjects
        # are created

        roomCenter = self.physicalSize / 2.0
        roombg = ro.RoomBg(roomCenter)
        roombg.add(self.allObjects)
        self.allObjects.change_layer(roombg,Level.ROOM_BG)

        box = ro.Crate((0,0))
        box.add(self.allObjects)
        self.allObjects.change_layer(box,Level.DYNAMIC)
        box = ro.Crate((0,10))
        box.add(self.allObjects)
        self.allObjects.change_layer(box,Level.DYNAMIC)
        print "Physical position: ",box.physicalPosition
        print "Rect: ",box.rect.center

    def update(self):
        '''
        Handles logic for a game step
        '''
        self.allObjects.update()

    def render(self,surface):
        '''
        Renders a game step after the logic is complete
        '''
        bg = surface.copy()
        bg.fill((255,255,255))
        self.allObjects.draw(surface,bg)

        if self.drawDebug:
            upperLeftCorner = Viewport().convertPhysicalToPixelCoords((0,self.physicalSize.y))
            size = self.physicalSize * PIXELS_PER_METER
            debugRect = pygame.Rect(upperLeftCorner,size)
            pygame.draw.rect(surface,(255,0,0),debugRect,1)