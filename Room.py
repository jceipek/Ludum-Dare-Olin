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
        self.Width = width
        self.Height = height
        self.Windows = list()
        self.Platforms = list()
        self.Doors = list()
        self.Lasers = list()
        self.Boxes = list()
        self.SpawnPoints = list()

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
        self.Height = height
        self.OnLeft = True
        self.DistanceFromBottom = distanceFromBottom

class Laser(object):
    def __init__(self,position):
        self.Position = position
        self.Activated = True
        self.Orientation = 0

class Turret(object):
    def __init__(self):
        self.Activated = True
        self.Orientation = 0

class StaticTurret(Turret):
    def __init__(self,position):
        super(StaticTurret,self).__init__()
        self.Position = position

class HangingTurret(Turret):
    def __init__(self,position,length,angle):
        super(HangingTurret,self).__init__()

        self.Position = position
        self.Length = length
        self.Angle = angle

class Rectangle(object):
    def __init__(self, width, height):
        self.Width = width
        self.Height = height

class StaticPlatform(Rectangle):
    def __init__(self, bottomLeftCorner, width, height):
        super(Rectangle,self).__init__(width,height)
        self.BottomLeftCorner = bottomLeftCorner