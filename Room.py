import os
from manager import *

class Room(object):
    '''
    Defines a room within the dungeon.

    A room has:
        windows
        platforms
    '''

    # Creates an empty room
    def __init__(self,width,height):
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

class Polygon(object):
    '''
    Defines a polygon with an arbitrary number of points.
    '''

    def __init__(self, *points):
        self.Points = tuple(points)

    def VertexCount(self):
        return len(self.Points)

class Window(Polygon):
    pass

class Door(object):
    def __init__(self, height, distanceFromBottom):
        self.height = height
        self.onLeft = True
        self.distanceFromBottom = distanceFromBottom

class Laser(object):
    def __init__(self,position):
        self.position = position
        self.activated = True
        self.orientation = 0

class Turret(object):
    def __init__(self):
        self.activated = True
        self.orientation = 0

class StaticTurret(Turret):
    def __init__(self,position):
        super(StaticTurret,self).__init__()
        self.position = position

class HangingTurret(Turret):
    def __init__(self,position,length,angle):
        super(HangingTurret,self).__init__()
        self.position = position
        self.length = length
        self.angle = angle

class Rectangle(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Box(object):
    def __init__(self, position, width, height):
        self.position = position
        self.width = width
        self.height = height
        self.body = None
        self.sprite = pygame.image.load(os.path.join('crate.png'))
        #Load image
    def add(self, w):
        bodyDef = b2BodyDef()
        bodyDef.position = self.position
        bodyDef.linearDamping = 0.2
        self.body = w.CreateBody(bodyDef)
        shapeDef = b2PolygonDef()
        shapeDef.SetAsBox(self.width, self.height)
        shapeDef.density = 0.4
        shapeDef.friction = 0.1
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()

        self.obj = pygame.Surface((self.width, self.height))
        self.obj = self.obj.convert()
        self.obj.blit(self.sprite, (0, 0))
    def getPosition(self):
        return ( (10 - self.body.position.x) * (640/10) + 640/20, (10 - self.body.position.y) * (480/10) + 480/20 )
    

class StaticPlatform(Rectangle):
    def __init__(self, bottomLeftCorner, width, height):
        super(Rectangle,self).__init__(width,height)
        self.BottomLeftCorner = bottomLeftCorner