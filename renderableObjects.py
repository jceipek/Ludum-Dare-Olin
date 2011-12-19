import pygame
from images import ImageHandler

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
        pass

    def __setPhysicalPosition(self,value):
        self.__physicalPosition = value
        #TODO: move pixel position

    def __getPhysicalPosition(self):
        return self.__physicalPosition

    physicalPosition = property(__getPhysicalPosition,__setPhysicalPosition)
    
    def __setPixelPosition(self,value):
        self.rect.move_ip(*value)
        # TODO: move physical position

    def __getPixelPosition(self):
        return (self.rect.left,self.rect.top)

    pixelPosition = property(__getPixelPosition,__setPixelPosition)

class Crate(RenderableObject):
    def __init__(self,position,imageName="crate"):
        RenderableObject.__init__(self,position,imageName)