import pygame
import renderableObjects as ro

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

    def __init__(self,filename):
        self.allObjects = pygame.sprite.LayeredDirty()


        box = ro.Crate((0,0))
        box.add(self.allObjects)

    def update(self):
        '''
        Handles logic for a game step
        '''
        pass

    def render(self,surface):
        '''
        Renders a game step after the logic is complete
        '''
        self.allObjects.draw(surface)