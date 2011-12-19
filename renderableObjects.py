import pygame
from images import ImageHandler
from viewport import Viewport

class RenderableObject(pygame.sprite.DirtySprite):

    def __init__(self,physicalPosition,imageName):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = ImageHandler()[imageName] # Returns a pygame surface

        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(0,0,width,height)

        self.physicalPosition = physicalPosition

    def update(self):
        '''
        Overrides Sprite update
        '''
        if Viewport().hasMoved:
            self.rect.center = Viewport().convertPhysicalToPixelCoords(self.__physicalPosition)
            self.dirty = 1

    def __setPhysicalPosition(self,value):
        self.__physicalPosition = value
        self.rect.center = Viewport().convertPhysicalToPixelCoords(value)

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
    def __init__(self,position,imageName="crate"):
        RenderableObject.__init__(self,position,imageName)

class RoomBg(RenderableObject):
    def __init__(self,position,imageName="roombg"):
        RenderableObject.__init__(self,position,imageName)