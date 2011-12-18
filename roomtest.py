from globals import *
import pygame
from pygame.locals import *
import room as rm
import manager as mgr
import dimension as dim

WIDGET_TOOLBAR_WIDTH = 200

widgetClasses = (rm.Box,)

class ImageToolbox:
    def __init__(self):
        self.surface = pygame.Surface((WIDGET_TOOLBAR_WIDTH, SCREEN_PIXEL_HEIGHT))
        self.surface.fill((0,0,0))
        self.images = list()
        self.hitboxes = list()
        
        horiz_padding = 10; #px
        vert_padding = 10; #px
        vert_position = 10; #px

        for cls in widgetClasses:
            obj = cls(pos=None)
            self.surface.blit(obj.sprite,(horiz_padding,vert_padding))
            vert_position += vert_padding

            top = vert_position;
            bottom = top + obj.sprite.get_height()
            left = horiz_padding + SCREEN_PIXEL_WIDTH
            right = left + obj.sprite.get_width()

            hitbox = PixelHitbox(top,bottom,left,right)

            self.images.append(obj)
            self.hitboxes.append(hitbox)

        self.surface = self.surface.convert()

    def FindClickedObject(self,pos):
        for i in xrange(len(self.hitboxes)):
            if self.hitboxes[i].InBox(pos):
                return self.images[i]

        return None

class PixelHitbox:
    def __init__(self,top,bottom,left,right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def InBox(self,pos):
        return self.left<= pos[0] <= self.right and self.top<= pos[1] <= self.bottom

class LevelDesigner:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((SCREEN_PIXEL_WIDTH + WIDGET_TOOLBAR_WIDTH,SCREEN_PIXEL_HEIGHT))
        self.room = rm.Room(SCREEN_REAL_WIDTH*10,SCREEN_REAL_HEIGHT*10)

        background = pygame.Surface((SCREEN_PIXEL_WIDTH,SCREEN_PIXEL_HEIGHT))
        background.fill((255,255,255))
        self.background = background.convert()
        self.surface.blit(background,(0,0))

        self.toolbox = ImageToolbox()
        self.surface.blit(self.toolbox.surface,(SCREEN_PIXEL_WIDTH,0))

        box = rm.Box(pos=dim.Vect(dim.Dimension(unitstr="1.0 m"),dim.Dimension(unitstr="1.0 m")))
        box.blitToInitialPosition(self.surface)
        self.room.boxes.append(box)

        print box.size

    def main(self):
        
        vp = mgr.ViewPort()
        movement = dim.Dimension(unitstr="1.0 m")
        zero = dim.Dimension(unitstr="0.0 m")

        while True:
            #for object in room.GetAllObjects():

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_UP:
                        print "Hit Up"
                        vp.originDelta = vp.originDelta + dim.Vect(zero,movement)
                    elif event.key == K_DOWN:
                        print "Hit Down"
                        vp.originDelta = vp.originDelta - dim.Vect(zero,movement)
                    elif event.key == K_RIGHT:
                        print "Hit Right"
                        vp.originDelta = vp.originDelta + dim.Vect(movement,zero)
                    elif event.key == K_LEFT:
                        print "Hit Left"
                        vp.originDelta = vp.originDelta - dim.Vect(movement,zero)
                elif event.type == MOUSEBUTTONDOWN:
                    print "Mouse Clicked at ",event.pos
                    print "Found object: ",self.toolbox.FindClickedObject(event.pos)

                
            self.surface.blit(self.background,(0,0))
            for item in self.room.GetAllObjects():
                item.blitToInitialPosition(self.surface)
            pygame.display.flip()
        
if (__name__ == "__main__"):
    LevelDesigner().main()