import pygame
import Box2D
import sys
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000,1000))

        self.activeLevel = Level(None)

    def main(self):

        self.running = True
        while self.running:
            self.processEventLoop()
            self.activeLevel.update()
            self.activeLevel.render(self.surface)
            pygame.display.flip()

    def processEventLoop(self):
        for e in pygame.event.get():
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    self.handleKey(event)
                elif event.type == MOUSEBUTTONDOWN:
                    self.handleClick(event)

    def handleClick(self,event):
        print "Mouse clicked at: ",event.pos

    def handleKey(self,event):
        if event.key == K_ESCAPE:
            return
        elif event.key == K_UP:
            print "Hit Up"
        elif event.key == K_DOWN:
            print "Hit Down"
        elif event.key == K_RIGHT:
            print "Hit Right"
        elif event.key == K_LEFT:
            print "Hit Left"

if __name__ == "__main__":
    Game().main()