from manager import *
from serializable import Serializable
import os
from images import ImageHandler
import manager as mgr
import dimension as dim

SPACEMAN_SIZE = dim.Vect(80*PIXEL,90*PIXEL).ConvertTo(METER)
BOX_SIZE = dim.Vect(76*PIXEL,78*PIXEL).ConvertTo(METER)

class RenderableObject(pygame.sprite.DirtySprite):
    def __init__(self, world, pos, size, spriteName, **kwargs):
        pygame.sprite.DirtySprite.__init__(self)

        self.body = None

        self.dirty = 1 #Specify that the image should be redrawn at start
        self.image = ImageHandler()[spriteName]

        #world.drawables.append(self)
        self.world = world
        self.vp = mgr.ViewPort()
        
        self.kieferSize = size
        self.initPosition = pos
        self.kwargs = kwargs

        if self.initPosition:
            initPos = self.initPosition.ConvertTo(PIXEL).Strip()
        else:
            initPos = (0,0)
        imageWidth = self.image.get_width()
        imageHeight = self.image.get_height()

        self.rect = pygame.Rect(initPos[0],initPos[1],imageWidth,imageHeight)
        self.old_rect = self.rect.copy()
        self.lastDrawPosition = dim.Vect(PIXEL*0,PIXEL*0) 

    def update(self,*args): # Override sprite update method
        # Do not blit here!!! Blitting happens with the sprite group!

        if self.body: #Check if we have a physics body
            bodyPos = dim.Vect(METER*self.body.position.x, METER*self.body.position.y)
        else:
            bodyPos = self.initPosition
        drawPos = bodyPos + (1.0/2.0) * self.kieferSize.MirrorH()

        # If the item has moved, set it as dirty
        if self.lastDrawPosition != drawPos:
            cornerPixelCoords = self.vp.ScreenCoords(drawPos).Strip()
            oldPixelCoords = self.vp.ScreenCoords(self.lastDrawPosition).Strip()

            # Properly place the old rectangle to blit
            self.old_rect.move_ip(*oldPixelCoords)

            # Properly place the new rectangle to blit
            self.rect = self.old_rect.move(*cornerPixelCoords)

            #Combine and set
            self.rect.union_ip(self.old_rect)

            dirty = 1
            self.lastDrawPosition = drawPos

    def add(self):
        self.prepPhysics(self.world)

    def prepPhysics(self,w):
        bodyDef = b2BodyDef()
        bodyDef.position = self.initPosition.ConvertTo(Dimension(unitstr="1.0 m")).Strip() #initPosition is a Vect
        bodyDef.fixedRotation = self.kwargs.get("fixedRotation", False)
        bodyDef.linearDamping = 0.15
        self.body = self.world.CreateBody(bodyDef)
        self.body.SetUserData(self.kwargs.get("userData", "object"));

        shapeDef = b2PolygonDef()
        shapeDef.SetAsBox(*(self.size / 2.0).ConvertTo(
            Dimension(unitstr="1.0 m")).Strip())
        shapeDef.density = self.kwargs.get("density", DENSITY)
        shapeDef.linearDamping = AIR_RESISTANCE
        shapeDef.friction = FRICTION
        
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()

    def blitToScreen(self,screen):
        '''
        Left for compatibility 
        XXX:Do not continue using this
        '''
        bodyPos = dim.Vect(METER*self.body.position.x, METER*self.body.position.y)
        drawPos = bodyPos + (1.0/2.0) * self.size.MirrorH()
        screen.blit(self.image, self.vp.ScreenCoords(drawPos).Strip())

    def blitToInitialPosition(self,screen):
        '''
        Blits to the initial position for this object
        Used by the level designer
        '''
        screen.blit(self.image,self.vp.ScreenCoords(self.initPosition).Strip())

    def getSize(self):
        if self.image == None:
            return None

        width = self.image.get_width()
        height = self.image.get_height()
        return mgr.Vect(mgr.Dimension(value=width,units="px"),mgr.Dimension(value=height,units="px"))


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
    def __init__(self, world=None, position=None):
        RenderableObject.__init__(self, world, position, BOX_SIZE, "crate")
 
class StaticPlatform(RenderableObject):
    def __init__(self, world, pos, size):
        RenderableObject.__init__(self, world, pos, size, spriteName="simplePlatform", density=0, userData="staticPlatform")

    def posVect(self):
        xr = self.body.position.x
        yr = self.body.position.y
        x = xr * METER
        y = yr * METER
        return dimension.Vect(x, y)

    def GetCorners(self):
        a = self.size/2.0
        #print a
        b = a.MirrorH()
        c = b.MirrorV()
        d = c.MirrorH()
        deltaP = self.posVect()
        corners = [a, b, c, d]
        for i in range(len(corners)):
            corners[i].Rotate(self.body.angle)
            corners[i] = corners[i] + deltaP
        return corners

    def blitToScreen(self, screen):
        corners = self.GetCorners()
        for i in range(len(corners) + 1):
            pos_start = self.vp.ScreenCoords(corners[i - 2]).Strip()
            pos_end = self.vp.ScreenCoords(corners[i - 1]).Strip()
            pygame.draw.line(screen, (255, 255, 255), pos_start, pos_end, 2)


class Spaceman(RenderableObject):
    def __init__(self, world, pos):
        RenderableObject.__init__(self, world, pos, SPACEMAN_SIZE, "walkingRight", userData="spaceman")

        self.IMG_COUNT = 30

        self.sprWalkR = ImageHandler()["walkingRight"]
        self.sprWalkL = ImageHandler()["walkingLeft"]

        # TODO: Figure out how to fix this
        self.inPixels = SPACEMAN_SIZE.ConvertTo(Dimension(value=1.0, units={'px': 1})).Strip()
        self.image = pygame.Surface(self.inPixels)
        self.image = self.image.convert_alpha()
        self.image.blit(self.sprWalkR, (0, 0))
        self.size = SPACEMAN_SIZE

        self.curVel = None
        self.touchingGround = 0
    def updateImg(self, background, loopcount):
        if abs(self.body.GetLinearVelocity().x) >= 0.2:
            self.image.blit(background, (0, 0))
            
            frameNo = loopcount % self.IMG_COUNT
            if self.body.GetLinearVelocity().x > 0: #Moving Right
                self.image.blit(self.sprWalkR, 
                              (-self.inPixels[0] * (frameNo), 0))  #Traverse the width of the image
            else:
                self.image.blit(self.sprWalkL, 
                              (-self.inPixels[0] * (frameNo), 0))
    def motionCheck(self):
        self.curVel = self.body.GetLinearVelocity()
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
