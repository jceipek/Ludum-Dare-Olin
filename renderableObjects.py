import pygame
import Box2D
from globals import *
from images import ImageHandler
from viewport import Viewport
from dimension import Vect

class RenderableObject(pygame.sprite.DirtySprite):

    def __init__(self,physicalPosition,physicsWorld,imageName,hasPhysics=True,isStatic=False,canRotate=True,userData=""):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = ImageHandler()[imageName] # Returns a pygame surface

        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(0,0,width,height)

        if not isinstance(physicalPosition, Vect):
            physicalPosition = Vect(*physicalPosition)
        self.physicalPosition = physicalPosition

        self.physicsWorld = physicsWorld
        self.hasPhysics = hasPhysics
        if self.hasPhysics:
            self._buildPhysics(width,height,canRotate,isStatic)
            self.body.SetUserData(userData)

    def _buildPhysics(self,width,height,canRotate,isStatic,friction=FRICTION):
        bodyDef = Box2D.b2BodyDef()
        bodyDef.position = (self.physicalPosition[0],self.physicalPosition[1])
        bodyDef.fixedRotation = not canRotate
        bodyDef.linearDamping = 0.15
        self.body = self.physicsWorld.CreateBody(bodyDef)
        #self.body.SetUserData(self)

        shapeDef = Box2D.b2PolygonDef()
        shapeDef.SetAsBox((width / 2.0) /  PIXELS_PER_METER, (height / 2.0) / PIXELS_PER_METER)
        if isStatic:
            shapeDef.density = 0
        else:
            shapeDef.density = DENSITY
        shapeDef.linearDamping = AIR_RESISTANCE
        shapeDef.friction = friction
        
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()

    def update(self, msSinceLast):
        '''
        Overrides Sprite update
        '''
        if Viewport().hasMoved:
            self.rect.center = Viewport().convertPhysicalToPixelCoords(self.__physicalPosition)
            self.dirty = 1
            
        if self.hasPhysics:
            newPhysicalPosition = Vect(self.body.position.x,self.body.position.y)
            if newPhysicalPosition != self.physicalPosition:
                self.physicalPosition = newPhysicalPosition

    def __setPhysicalPosition(self,value):
        self.__physicalPosition = value
        self.rect.center = Viewport().convertPhysicalToPixelCoords(value)
        self.dirty = 1

    def __getPhysicalPosition(self):
        return self.__physicalPosition

    physicalPosition = property(__getPhysicalPosition,__setPhysicalPosition)
    
    def __setPixelPosition(self,value):
        self.rect.move_ip(*value)
        self.__physicalPosition = Viewport().convertPixelsToPhysicalCoords(self.rect.center)

    def __getPixelPosition(self):
        return (self.rect.left,self.rect.top)

    pixelPosition = property(__getPixelPosition,__setPixelPosition)

class Crate(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="crate"):
        RenderableObject.__init__(self,position,physicsWorld,imageName)

class RoomBg(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="roombg"):
        RenderableObject.__init__(self,position,physicsWorld,imageName,hasPhysics=False)

class Platform(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="simplePlatform"):
        RenderableObject.__init__(self,position,physicsWorld,imageName,hasPhysics=True,isStatic=True,canRotate=False,userData="platform")

class Spaceman(RenderableObject):

    STANDING_RIGHT = 0
    STANDING_LEFT = 1
    WALKING_RIGHT = 2
    WALKING_LEFT = 3
    JUMPING_RIGHT = 4
    JUMPING_LEFT = 5

    def __init__(self,position,physicsWorld):
        pygame.sprite.DirtySprite.__init__(self)
        self.spriteSheetRight = ImageHandler()["walkingRight"] # Returns a pygame surface
        self.spriteSheetLeft = ImageHandler()["walkingLeft"] # Returns a pygame surface
        self.spriteSheetJumpR = ImageHandler()["jumpingRight"] # Returns a pygame surface
        self.spriteSheetJumpL = ImageHandler()["jumpingLeft"] # Returns a pygame surface
       
        self.curVel  = (0,0)

        sprite_height = 90
        sprite_width = 80

        self.rect = pygame.Rect(0,0,sprite_width,sprite_height)

        if not isinstance(position, Vect):
            physicalPosition = Vect(*position)
        self.physicalPosition = position

        self.physicsWorld = physicsWorld

        self.spritesRight = list()
        self.spritesLeft  = list()
        self.sprJumpingRight  = list()
        self.sprJumpingLeft  = list()
        self.sprStandingRight = ImageHandler()["standingRight"]
        self.sprStandingLeft = ImageHandler()["standingLeft"]

        for i in xrange(self.spriteSheetRight.get_width() // sprite_width):
            newSprite = pygame.Surface((sprite_width,sprite_height),pygame.SRCALPHA,32)
            area = pygame.Rect(i*sprite_width,0,sprite_width,sprite_height)
            newSprite.blit(self.spriteSheetRight, (0,0), area)
            newSprite.convert()
            self.spritesRight.append(newSprite)

        for i in xrange(self.spriteSheetLeft.get_width() // sprite_width):
            newSprite = pygame.Surface((sprite_width,sprite_height),pygame.SRCALPHA,32)
            area = pygame.Rect(i*sprite_width,0,sprite_width,sprite_height)
            newSprite.blit(self.spriteSheetLeft, (0,0), area)
            newSprite.convert()
            self.spritesLeft.append(newSprite)
        
        for i in xrange(20):
            newSprite = pygame.Surface((sprite_width,sprite_height),pygame.SRCALPHA,32)
            area = pygame.Rect(i*sprite_width,0,sprite_width,sprite_height)
            newSprite.blit(self.spriteSheetJumpR, (0,0), area)
            newSprite.convert()
            self.sprJumpingRight.append(newSprite)

        for i in xrange(20):
            newSprite = pygame.Surface((sprite_width,sprite_height),pygame.SRCALPHA,32)
            area = pygame.Rect(i*sprite_width,0,sprite_width,sprite_height)
            newSprite.blit(self.spriteSheetJumpL, (0,0), area)
            newSprite.convert()
            self.sprJumpingLeft.append(newSprite)


        self.spriteIndex = 0.0
        #self.image = self.spritesRight[int(self.spriteIndex)]
        self.image = ImageHandler()["standingRight"]

        self.hasPhysics = True
        self._buildPhysics(width=sprite_width/2.0,height=sprite_height,canRotate=False,isStatic=False)
        self.body.SetUserData("spaceman")

        self.animstate = Spaceman.STANDING_RIGHT

        self.touchingGround = 0
        self.tryingToJump = False

        
    def update(self, msSinceLast):
        '''
        Overrides Sprite update
        '''
        if Viewport().hasMoved:
            self.rect.center = Viewport().convertPhysicalToPixelCoords(self.__physicalPosition)
            self.dirty = 1
            
        if self.hasPhysics:
            newPhysicalPosition = Vect(self.body.position.x,self.body.position.y)
            if newPhysicalPosition != self.physicalPosition:
                self.physicalPosition = newPhysicalPosition


        getVel = self.body.GetLinearVelocity()
        self.curVel = (getVel.x, getVel.y)
        if self.curVel[0] >= -2.0 and self.curVel[0] < 0.0:
            self.tryStop()
            self.animstate = Spaceman.STANDING_LEFT
        elif self.curVel[0] <= 2.0 and self.curVel[0] > 0.0:
            self.tryStop()
            self.animstate = Spaceman.STANDING_RIGHT
        elif self.curVel[0] > 2.0:
            if self.isOnGround():
                self.animstate = Spaceman.WALKING_RIGHT
            elif self.tryingToJump:
                self.animstate = Spaceman.JUMPING_RIGHT
            else:
                self.animstate = Spaceman.STANDING_RIGHT
        elif self.curVel[0] < -2.0:
            if self.isOnGround():
                self.animstate = Spaceman.WALKING_LEFT
            elif self.tryingToJump:
                self.animstate = Spaceman.JUMPING_LEFT
            else:
                self.animstate = Spaceman.STANDING_LEFT

        self.spriteIndex += (msSinceLast/33.0)
        if self.animstate == Spaceman.WALKING_RIGHT:
            self.image = self.spritesRight[int(self.spriteIndex%len(self.spritesRight))]
        elif self.animstate == Spaceman.WALKING_LEFT:
            self.image = self.spritesLeft[int(self.spriteIndex%len(self.spritesLeft))]
        elif self.animstate == Spaceman.JUMPING_RIGHT:
            index = int(self.spriteIndex%len(self.sprJumpingRight))
            if self.spriteIndex>len(self.sprJumpingRight)/2:
                index = len(self.sprJumpingRight)/2
            self.image = self.sprJumpingRight[index]
        elif self.animstate == Spaceman.JUMPING_LEFT:
            index = int(self.spriteIndex%len(self.sprJumpingLeft))
            if self.spriteIndex>len(self.sprJumpingLeft)/2:
                index = len(self.sprJumpingLeft)/2
            self.image = self.sprJumpingLeft[index]
        elif self.animstate == Spaceman.STANDING_RIGHT:
            self.image = ImageHandler()["standingRight"]
        elif self.animstate == Spaceman.STANDING_LEFT:
            self.image = ImageHandler()["standingLeft"]            

    def tryMove(self, x, y):
        self.curVel = self.body.GetLinearVelocity()
        
        if x < 0 and self.curVel.x > -MAX_WALK_SPEED: #Not going too fast Left
            if self.curVel.x+x/(FPS*self.body.GetMass()) > -MAX_WALK_SPEED: #You can accelerate all the way asked
                self.body.ApplyForce(Box2D.b2Vec2(x,0), self.body.GetWorldCenter())
            else: #You can only accelerate to the max walk speed
                self.body.ApplyForce(Box2D.b2Vec2(FPS*(-MAX_WALK_SPEED-self.curVel.x)*self.body.GetMass(),0), self.body.GetWorldCenter())
        elif x > 0 and self.curVel.x < MAX_WALK_SPEED: #Not going too fast Right
            if self.curVel.x+x/(FPS*self.body.GetMass()) < MAX_WALK_SPEED: #You can accelerate all the way asked
                self.body.ApplyForce(Box2D.b2Vec2(x,0), self.body.GetWorldCenter())
            else: #You can only accelerate to the max walk speed
                self.body.ApplyForce(Box2D.b2Vec2(FPS*(MAX_WALK_SPEED-self.curVel.x)*self.body.GetMass(),0), self.body.GetWorldCenter())
    
    def tryStop(self, horiz=True, vert=False):
        print "trying to stop"
        self.curVel = self.body.GetLinearVelocity()
        if horiz:
            self.body.ApplyForce(Box2D.b2Vec2(FPS*(-self.curVel.x)*self.body.GetMass(),0), self.body.GetWorldCenter())
        if vert:
            self.body.ApplyForce(Box2D.b2Vec2(0,FPS*(-self.curVel.y)*self.body.GetMass()), self.body.GetWorldCenter())
    
    def isOnGround(self):
        return self.touchingGround>0

class TheSpaceman(Spaceman):
    _instance = None
    _init = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(TheSpaceman, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance
    def __init__(self,position=None,physicsWorld=None):
        if not TheSpaceman._init:
            Spaceman.__init__(self,position,physicsWorld)
            TheSpaceman._init = True
