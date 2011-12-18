from globals import *
import pygame
from pygame.locals import *
import room as rm

WIDGET_TOOLBAR_WIDTH = 200

class LevelDesigner:
    def __init__(self):
        pygame.init()

        surface = pygame.display.set_mode((SCREEN_PIXEL_WIDTH + WIDGET_TOOLBAR_WIDTH,SCREEN_PIXEL_HEIGHT))
        room = rm.Room(SCREEN_REAL_WIDTH,SCREEN_REAL_HEIGHT)

        box = rm.Box(position=(10,10))
        box.blitToScreen(surface)
        
    def main(self):
        

        while True:
            #for object in room.GetAllObjects():

            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_UP:
                        pass
                    elif event.key == K_DOWN:
                        pass
                    elif event.key == K_RIGHT:
                        pass
                    elif event.key == K_LEFT:
                        pass
                elif event.type == MOUSEBUTTONDOWN:
                    pass #handle hitting the right sprite here
                pygame.display.flip()
        
if (__name__ == "__main__"):
    LevelDesigner().main()