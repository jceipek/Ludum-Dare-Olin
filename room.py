from manager import *
from serializable import Serializable
import os
from images import ImageHandler
import manager as mgr
import dimension as dim

pixel = dim.Dimension(value=1.0, units={'px': 1})
SPACEMAN_SIZE = dim.Vect(80*pixel,90*pixel)
BOX_SIZE = dim.Vect(76*pixel,78*pixel)

class RenderableObject(object):
    def __init__(self, world, pos, size, **kwargs):
        self.sprite = None #Sprite loading is done in subclass

        #world.drawables.append(self)
        self.world = world
        self.vp = mgr.ViewPort()
        
        self.size = size
        self.position = pos
        self.kwargs = kwargs

    def add(self):
        self.prepPhysics(self.world)

    def prepPhysics(self,w):
        bodyDef = b2BodyDef()
        bodyDef.position = self.position.ConvertTo(Dimension(unitstr="1.0 m")).Strip() #position is a Vect
        bodyDef.fixedRotation = self.kwargs.get("fixedRotation", False)
        bodyDef.linearDamping = 0.15
        self.body = self.world.CreateBody(bodyDef)

        shapeDef = b2PolygonDef()
        shapeDef.SetAsBox(*(self.size / 2.0).ConvertTo(
            Dimension(unitstr="1.0 m")).Strip())
        shapeDef.density = self.kwargs.get("density", DENSITY)
        shapeDef.linearDamping = AIR_RESISTANCE
        shapeDef.friction = FRICTION
        
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()

    def blitToScreen(self,screen):
        screen.blit(self.sprite,self.vp.ScreenCoords(dim.Vect(METER*self.body.position.x, METER*self.body.position.y)).Strip())

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
    def __init__(self, world=None, pos=pixel):
        RenderableObject.__init__(self, world, pos, BOX_SIZE)

        self.sprite = ImageHandler()["crate"]
 

class StaticPlatform(RenderableObject):
    def __init__(self, world, pos, size):
        RenderableObject.__init__(self, world, pos, (width,height), density=0)
        self.BottomLeftCorner = bottomLeftCorner

    def blitToScreen(self, screen):
        corners = self.GetCorners()
        for i in range(len(corners) + 1):
            pos_start = self.vp.ScreenCoords(corners[i - 2]).Strip()
            pos_end = self.vp.ScreenCoords(corners[i - 1]).Strip()
            pygame.draw.line(screen, (255, 255, 255), pos_start, pos_end, 2)


class Spaceman(RenderableObject):
    def __init__(self, world, pos):
        RenderableObject.__init__(self, world, pos, SPACEMAN_SIZE)

        self.IMG_COUNT = 30

        self.sprWalkR = ImageHandler()["walkingRight"]
        self.sprWalkL = ImageHandler()["walkingLeft"]

        self.inPixels = SPACEMAN_SIZE.ConvertTo(Dimension(value=1.0, units={'px': 1})).Strip()
        self.sprite = pygame.Surface(self.inPixels)
        self.sprite = self.sprite.convert()
        self.sprite.blit(self.sprWalkR, (0, 0))

        self.curVel = None
    def updateImg(self, background, loopcount):
        if abs(self.body.GetLinearVelocity().x) >= 0.2:
            self.sprite.blit(background, (0, 0))
            
            frameNo = loopcount % self.IMG_COUNT
            if self.body.GetLinearVelocity().x > 0: #Moving Right
                self.sprite.blit(self.sprWalkR, 
                              (-self.inPixels[0] * (frameNo), 0))  #Traverse the width of the image
            else:
                self.sprite.blit(self.sprWalkL, 
                              (-self.inPixels[0] * (frameNo), 0))
    def motionCheck(self):
        self.curVel = self.body.GetLinearVelocity()
        print self.curVel
    def tryMove(self, x, y):
        if x < 0 and self.curVel.x > -MAX_WALK_SPEED: #Not going too fast Left
            if self.curVel.x+x/(FPS*self.body.GetMass()) > -MAX_WALK_SPEED: #You can accelerate all the way asked
                self.body.ApplyForce(b2Vec2(x,0), self.body.GetWorldCenter())
            else: #You can only accelerate to the max walk speed
                self.body.ApplyForce(b2Vec2(FPS*(-MAX_WALK_SPEED-self.curVel.x)*self.body.GetMass(),0), self.body.GetWorldCenter())
        elif x > 0 and self.curVel.x < MAX_WALK_SPEED: #Not going too fast Right
            if self.curVel.x+x/(FPS*self.body.GetMass()) < MAX_WALK_SPEED: #You can accelerate all the way asked
                self.body.ApplyForce(b2Vec2(x,0), self.body.GetWorldCenter())
            else: #You can only accelerate to the max walk speed
                self.body.ApplyForce(b2Vec2(FPS*(MAX_WALK_SPEED-self.curVel.x)*self.body.GetMass(),0), self.body.GetWorldCenter())