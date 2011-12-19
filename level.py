import pygame
import renderableObjects as ro
from dimension import Vect
from viewport import Viewport
from globals import *
from images import ImageHandler
import Box2D

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

        world_bounds = Box2D.b2AABB()
        world_bounds.lowerBound = (0,0)
        world_bounds.upperBound = (self.physicalSize[0],self.physicalSize[1])
        doSleep = True
        self.physicsWorld = Box2D.b2World(world_bounds, GRAVITY, doSleep)

    def setup(self):
        # Separate setup function such that Level properties
        # such as physical size can be read before RenderableObjects
        # are created

        roomCenter = self.physicalSize / 2.0
        roombg = ro.RoomBg(roomCenter,self.physicsWorld)
        roombg.add(self.allObjects)
        self.allObjects.change_layer(roombg,Level.ROOM_BG)

        box = ro.Crate((10,10),self.physicsWorld)
        box.add(self.allObjects)
        self.allObjects.change_layer(box,Level.DYNAMIC)
        #box = ro.Crate((20,10),self.physicsWorld)
        #box.add(self.allObjects)
        #self.allObjects.change_layer(box,Level.DYNAMIC)
        print "Physical position: ",box.physicalPosition
        print "Rect: ",box.rect.center

    def update(self):
        '''
        Handles logic for a game step
        '''
        self.physicsWorld.Step(1.0/60,10,8)
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