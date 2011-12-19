import pygame
import Box2D
from globals import *
from images import ImageHandler
from viewport import Viewport
from dimension import Vect

class RenderableObject(pygame.sprite.DirtySprite):

    def __init__(self,physicalPosition,physicsWorld,imageName,hasPhysics=True,canRotate=True):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = ImageHandler()[imageName] # Returns a pygame surface

        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(0,0,width,height)

        if not isinstance(physicalPosition, Vect):
            physicalPosition = Vect(*physicalPosition)
        self.physicalPosition = physicalPosition

        self.physicsWorld = physicsWorld
        self.hasPhysics = hasPhysics

        if self.hasPhysics:
            bodyDef = Box2D.b2BodyDef()
            bodyDef.position = (self.physicalPosition[0],self.physicalPosition[1])
            bodyDef.fixedRotation = not canRotate
            bodyDef.linearDamping = 0.15
            self.body = self.physicsWorld.CreateBody(bodyDef)
            #self.body.SetUserData(self)

            shapeDef = Box2D.b2PolygonDef()
            shapeDef.SetAsBox(width / 2.0 /  PIXELS_PER_METER, height / 2.0 / PIXELS_PER_METER)
            shapeDef.density = DENSITY
            shapeDef.linearDamping = AIR_RESISTANCE
            shapeDef.friction = FRICTION
        
            self.body.CreateShape(shapeDef)
            self.body.SetMassFromShapes()

    def update(self):
        '''
        Overrides Sprite update
        '''
        if Viewport().hasMoved:
            self.rect.center = Viewport().convertPhysicalToPixelCoords(self.__physicalPosition)
            self.dirty = 1
            
        if self.hasPhysics:
            if newPhysicalPosition != self.physicalPosition:
                self.dirty = 1
                self.physicalPosition = newPhysicalPosition

    def __setPhysicalPosition(self,value):
        self.__physicalPosition = value
        self.rect.center = Viewport().convertPhysicalToPixelCoords(value)
        self.dirty = 1

    def __getPhysicalPosition(self):
        return self.__physicalPosition

    physicalPosition = property(__getPhysicalPosition,__setPhysicalPosition)
    
    def __setPixelPosition(self,value):
        self.rect.move_ip(*value)
        self.__physicalPosition = Viewport().convertPixelsToPhysicalCoords(self.rect.center)

    def __getPixelPosition(self):
        return (self.rect.left,self.rect.top)

    pixelPosition = property(__getPixelPosition,__setPixelPosition)

class Crate(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="crate"):
        RenderableObject.__init__(self,position,physicsWorld,imageName)

class RoomBg(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="roombg"):
        RenderableObject.__init__(self,position,physicsWorld,imageName,hasPhysics=False)