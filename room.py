from manager import *
from serializable import Serializable
import os
from images import ImageHandler
import manager as mgr

class RenderableObject(object):
    def __init__(self):
        self.sprite = None #Sprite loading is done in superclass
        self.position = mgr.Vect(0,0,"meters")

    def add(self,w):
        self.prepPhysics(w)
        self.prepGraphics()

    def prepPhysics(self,w):
        bodyDef = b2BodyDef()
        bodyDef.position = self.realPosition
        bodyDef.linearDamping = 0.2
        self.body = w.CreateBody(bodyDef)
        shapeDef = b2PolygonDef()
        shapeDef.SetAsBox(self.realSize[0], self.realSize[1])
        shapeDef.density = 0.4
        shapeDef.friction = 0.1
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()

    def prepGraphics(self):
        self.obj = self.sprite
        #@Belland: is there any reason  to reblit here? I've changed this and self.obj should be eliminated
        '''
        self.obj = pygame.Surface((self.width, self.height))
        self.obj = self.obj.convert()
        self.obj.blit(self.sprite, (0, 0))
        '''

    def blitToScreen(self,screen):
        screen.blit(self.sprite,self.position.pixelsTuple())

    def getRealMeasurements(self):
        width = self.sprite.get_width() / PIXELS_PER_METER
        height = self.sprite.get_height() / PIXELS_PER_METER
        return (width,height)

class Room(Serializable):
    '''
    Defines a room within the dungeon.

    A room has:
        windows
        platforms
    '''

    # Creates an empty room
    def __init__(self,width=None,height=None):
        self.width = width
        self.height = height
        self.windows = list()
        self.platforms = list()
        self.doors = list()
        self.lasers = list()
        self.boxes = list()
        self.spawnPoints = list()
    
    def GetAllObjects(self):
        return self.windows+self.platforms+self.doors+self.lasers+self.boxes+self.spawnPoints

class Polygon(Serializable):
    '''
    Defines a polygon with an arbitrary number of points.
    '''

    def __init__(self, points=None):
        self.Points = points

    def VertexCount(self):
        return len(self.Points)

class Window(Polygon):
    pass

class Door(Serializable):
    def __init__(self, height=None, distanceFromBottom=None):
        self.height = height
        self.onLeft = True
        self.distanceFromBottom = distanceFromBottom

class Laser(Serializable):
    def __init__(self,position=None):
        super(Laser,self).__init__()
        self.position = position
        self.activated = True
        self.orientation = 0

class Turret(Serializable):
    def __init__(self):
        self.activated = True
        self.orientation = 0

class StaticTurret(Turret):
    def __init__(self,position=None):
        super(StaticTurret,self).__init__()
        self.position = position

class HangingTurret(Turret):
    def __init__(self,position=None,length=None,angle=None):
        super(HangingTurret,self).__init__()
        self.position = position
        self.length = length
        self.angle = angle

class Rectangle(Serializable):
    def __init__(self, width=None, height=None):
        self.width = width
        self.height = height

class Box(Serializable,RenderableObject):
    def __init__(self, realPosition=(0,0)):
        self.position = mgr.Vect(realPosition[0],realPosition[1],"meters")
        self.body = None
        self.sprite = ImageHandler()["crate.png"]
        self.size = self.getRealMeasurements() #TODO: update w/ Kiefer's size thing

        #Load image
    def getPosition(self):
        # Use self.realSize from now on

        #FIXME Box has a size use that, world has a size, use that. basically 
        #this entire function needs to be rewritten.
        return ( (10 - self.body.position.x) * (640/10) + 640/20, (10 - self.body.position.y) * (480/10) + 480/20 )
 

class StaticPlatform(Rectangle):
    def __init__(self, bottomLeftCorner=None, width=None, height=None):
        super(Rectangle,self).__init__(width,height)
        self.BottomLeftCorner = bottomLeftCorner
