import pygame
import Box2D
import sys
from globals import *
from level import Level
from viewport import Viewport
from images import ImageHandler

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((SCREEN_PIXEL_WIDTH,SCREEN_PIXEL_HEIGHT))
        self.loadLevel("roombg")
        #self.activeLevel.drawDebug = True
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load("title.mp3")
        pygame.mixer.music.play(-1)

    def main(self):

        self.running = True
        self.state = "INTRO"
               
        msSinceLast = 0

        intro = self.image = ImageHandler()["start"]
        self.surface.blit(intro, (0,0))
        pygame.display.flip()
        
        while self.running and self.state == "INTRO":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.state = "PLAYING"
        pygame.mixer.music.stop()
        pygame.mixer.music.load("alone2.mp3") 
        pygame.mixer.music.play(-1)

        while self.running and self.state == "PLAYING":
            self.processEventLoop()
            self.activeLevel.update(msSinceLast)
            msSinceLast = self.clock.tick(FRAMERATE)
            self.activeLevel.render(self.surface)
            pygame.display.flip()
            Viewport().hasMoved = False

    def processEventLoop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.handleKeyDown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handleClick(event)
        self.handleKeyState(pygame.key.get_pressed())

    def handleClick(self,event):
        print "Mouse clicked at: ",event.pos

    def handleKeyDown(self,event):
        vp = Viewport()
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_UP:
            self.activeLevel.characterJump()
            #vp.move((0,50))
        elif event.key == pygame.K_w:
            self.activeLevel.moveShip(0,5)
        elif event.key == pygame.K_s:
            self.activeLevel.moveShip(0,-5)
        elif event.key == pygame.K_d:
            self.activeLevel.moveShip(5,0)
        elif event.key == pygame.K_a:
            self.activeLevel.moveShip(-5,0)



    def handleKeyState(self,keys):
        if keys[pygame.K_RIGHT]:
            self.activeLevel.characterRight()
        if keys[pygame.K_LEFT]:
            self.activeLevel.characterLeft()

    def loadLevel(self,filename=None):
        self.activeLevel = Level(filename)
        Viewport().levelHeight = self.activeLevel.physicalSize.y
        self.activeLevel.setup()

if __name__ == "__main__":
    Game().main()
