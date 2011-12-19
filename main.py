import pygame
import Box2D
import sys
from globals import *
from level import Level
from viewport import Viewport

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((SCREEN_PIXEL_WIDTH,SCREEN_PIXEL_HEIGHT))
        self.loadLevel("roombg")
        self.activeLevel.drawDebug = True
        self.clock = pygame.time.Clock()

    def main(self):

        self.running = True
        while self.running:
            self.processEventLoop()
            self.activeLevel.update()
            self.clock.tick(FRAMERATE)
            self.activeLevel.render(self.surface)
            pygame.display.flip()
            Viewport().hasMoved = False

    def processEventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handleKey(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(event)

    def handleClick(self,event):
        print "Mouse clicked at: ",event.pos

    def handleKey(self,event):
        vp = Viewport()
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_UP:
            print "Hit Up"
            vp.move((0,50))
        elif event.key == pygame.K_DOWN:
            print "Hit Down"
            vp.move((0,-50))
        elif event.key == pygame.K_RIGHT:
            print "Hit Right"
            vp.move((-50,0))
        elif event.key == pygame.K_LEFT:
            print "Hit Left"
            vp.move((50,0))

    def loadLevel(self,filename=None):
        self.activeLevel = Level(filename)
        Viewport().levelHeight = self.activeLevel.physicalSize.y
        self.activeLevel.setup()

if __name__ == "__main__":
    Game().main()