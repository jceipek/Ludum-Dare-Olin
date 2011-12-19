from globals import *
import pygame
from pygame.locals import *
import room as rm
import manager as mgr
import dimension as dim
import copy

WIDGET_TOOLBAR_WIDTH = 200

# Specifies the widget classes we have
widgetClasses = (rm.Box,)#,rm.HangingTurret)

class ImageToolbox:
    def __init__(self):
        # Creates a surface to hold all the images
        self.surface = pygame.Surface((WIDGET_TOOLBAR_WIDTH, SCREEN_PIXEL_HEIGHT))
        self.surface.fill((100,100,100))
        self.images = list()
        self.hitboxes = list()
        
        horiz_padding = 10; #px
        vert_padding = 10; #px
        vert_position = 10; #px

        # Loads all images and blits them to the appropriate surface
        for cls in widgetClasses:
            obj = cls(position=None)
            self.surface.blit(obj.image,(horiz_padding,vert_position))

            top = vert_position;
            bottom = top + obj.image.get_height()
            left = horiz_padding + SCREEN_PIXEL_WIDTH
            right = left + obj.image.get_width()

            hitbox = PixelHitbox(top,bottom,left,right)

            self.images.append(obj)
            self.hitboxes.append(hitbox)

            vert_position = bottom + vert_padding

        self.surface = self.surface.convert()

    def findClickedObject(self,pos):
        # Find the object you clicked, based on the mouse pos passed in
        for i in xrange(len(self.hitboxes)):
            if self.hitboxes[i].inBox(pos):
                return self.images[i]

        return None

class PixelHitbox:
    def __init__(self,top,bottom,left,right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

    def inBox(self,pos):
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

        box = rm.Box(position=dim.Vect(dim.Dimension(unitstr="1.0 m"),dim.Dimension(unitstr="1.0 m")))
        box.blitToInitialPosition(self.surface)
        self.room.boxes.append(box)

        self.selectedItem = None

        print box.rect

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
                    self.handleClick(event.pos)
                
            self.surface.blit(self.background,(0,0))
            for item in self.room.GetAllObjects():
                item.blitToInitialPosition(self.surface)
                

            self.surface.blit(self.toolbox.surface,(SCREEN_PIXEL_WIDTH,0))

            if self.selectedItem:
                self.surface.blit(self.selectedItem.image,pygame.mouse.get_pos())
            pygame.display.flip()

    def handleClick(self,pos):
        print "Mouse Clicked at ", pos
        if self.clickInToolbox(pos):
            if not self.selectedItem:
                clickedObj = self.toolbox.findClickedObject(pos)
                print "Found object: ",clickedObj
                self.selectedItem = copy.deepcopy(clickedObj) # Copy pointer to image surface, and replace it. \
                                                                     # This is to work around the fact that deepcopy 
                                                                     # will make a dead surface
                self.selectedItem.image = clickedObj.image

            else:
                if self.selectedItem in self.room.boxes:
                    self.room.boxes.remove(self.selectedItem)  #Trash the object we have selected
                self.selectedItem = None # Deselect the current object

        else: 
            if self.selectedItem:
                pos = dim.Vect(PIXEL * pos[0], PIXEL * pos[1])
                physxCoord = mgr.ViewPort().PhysxCoords(pos)
                # We want to place the object
                self.selectedItem.initPosition = physxCoord
                #self.selectedItem.update()
                if not self.selectedItem in self.room.boxes:
                    self.room.boxes.append(self.selectedItem)
                self.selectedItem = None
            else:
                # We want to select the object here
                self.selectedItem = self.findClickedObject(pos) #Oops, this only works for stuff in the toolbox...
                print "Found object to move: ",self.selectedItem

    def clickInToolbox(self,pos):
        return pos[0] > SCREEN_PIXEL_WIDTH

    def findClickedObject(self, pos):
        for b in self.room.boxes:
            print b.rect.x,b.rect.y
            if b.rect.collidepoint(pos):
                return b
        return None
        
if (__name__ == "__main__"):
    LevelDesigner().main()
