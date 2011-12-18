from globals import *
import pygame
from pygame.locals import *
import room as rm
import manager as mgr
import dimension as dim

WIDGET_TOOLBAR_WIDTH = 200

class LevelDesigner:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((SCREEN_PIXEL_WIDTH + WIDGET_TOOLBAR_WIDTH,SCREEN_PIXEL_HEIGHT))
        self.room = rm.Room(SCREEN_REAL_WIDTH*10,SCREEN_REAL_HEIGHT*10)

        background = self.surface.copy()
        background.fill((255,255,255))
        self.background = background.convert()
        self.surface.blit(background,(0,0))

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
                        vp.originDelta = vp.originDelta + dim.Vect(movement,zero)
                    elif event.key == K_DOWN:
                        print "Hit Down"
                        vp.originDelta = vp.originDelta - dim.Vect(movement,zero)
                    elif event.key == K_RIGHT:
                        print "Hit Right"
                        vp.originDelta = vp.originDelta + dim.Vect(zero,movement)
                    elif event.key == K_LEFT:
                        print "Hit Left"
                        vp.originDelta = vp.originDelta - dim.Vect(zero,movement)
                elif event.type == MOUSEBUTTONDOWN:
                    pass #handle hitting the right sprite here

                
            self.surface.blit(self.background,(0,0))
            for item in self.room.GetAllObjects():
                item.blitToInitialPosition(self.surface)
            pygame.display.flip()
        
if (__name__ == "__main__"):
    LevelDesigner().main()