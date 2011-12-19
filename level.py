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


        self.background = None
        #self.background = pygame.Surface((SCREEN_PIXEL_WIDTH,SCREEN_PIXEL_HEIGHT))
        #self.background.fill((0,0,0))
        #self.background = self.background.convert()

    def setup(self):
        # Separate setup function such that Level properties
        # such as physical size can be read before RenderableObjects
        # are created

        roomCenter = self.physicalSize / 2.0
        roombg = ro.RoomBg(roomCenter,self.physicsWorld)
        roombg.add(self.allObjects)
        self.allObjects.change_layer(roombg,Level.ROOM_BG)

        '''
        box = ro.Crate((10,10),self.physicsWorld)
        box.add(self.allObjects)
        self.allObjects.change_layer(box,Level.DYNAMIC)
        box = ro.Crate((10,15),self.physicsWorld)
        box.add(self.allObjects)
        self.allObjects.change_layer(box,Level.DYNAMIC)
        '''

        platform = ro.Platform((10,5),self.physicsWorld)
        platform.add(self.allObjects)
        self.allObjects.change_layer(platform,Level.FIXED)

        for x in xrange(2,25,4):
            platform = ro.Platform((x, 1),self.physicsWorld)
            platform.add(self.allObjects)
            self.allObjects.change_layer(platform,Level.FIXED)        

        self.spaceman = ro.Spaceman((10,10),self.physicsWorld)
        self.spaceman.add(self.allObjects)
        self.allObjects.change_layer(self.spaceman, Level.DYNAMIC)
        
    def update(self, msSinceLast):
        '''
        Handles logic for a game step
        '''
        self.physicsWorld.Step(1.0/60,10,8)
        self.allObjects.update(msSinceLast)

    def render(self,surface):
        '''
        Renders a game step after the logic is complete
        '''
        self.allObjects.draw(surface,self.background)

        if self.drawDebug:
            upperLeftCorner = Viewport().convertPhysicalToPixelCoords((0,self.physicalSize.y))
            size = self.physicalSize * PIXELS_PER_METER
            debugRect = pygame.Rect(upperLeftCorner,size)
            pygame.draw.rect(surface,(255,0,0),debugRect,1)

    def characterRight(self):
        self.spaceman.tryMove(600,0)
    def characterLeft(self):
        self.spaceman.tryMove(-600,0)
    def characterJump(self):
        self.spaceman.tryMove(0,600)

