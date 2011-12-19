import pygame
import Box2D
from globals import *
from images import ImageHandler
from viewport import Viewport
from dimension import Vect

class RenderableObject(pygame.sprite.DirtySprite):

    def __init__(self,physicalPosition,physicsWorld,imageName,hasPhysics=True,isStatic=False,canRotate=True):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = ImageHandler()[imageName] # Returns a pygame surface

        width = self.image.get_width()
        height = self.image.get_height()
        self.rect = pygame.Rect(0,0,width,height)

        if not isinstance(physicalPosition, Vect):
            physicalPosition = Vect(*physicalPosition)
        self._setPhysicalPosition(physicalPosition)

        self.physicsWorld = physicsWorld
        self.hasPhysics = hasPhysics
        if self.hasPhysics:
            self._buildPhysics(width,height,canRotate,isStatic)

    def _buildPhysics(self,width,height,canRotate,isStatic):
        bodyDef = Box2D.b2BodyDef()
        bodyDef.position = (self.physicalPosition[0],self.physicalPosition[1])
        bodyDef.fixedRotation = not canRotate
        bodyDef.linearDamping = AIR_RESISTANCE
        self.body = self.physicsWorld.CreateBody(bodyDef)
        #self.body.SetUserData(self)

        shapeDef = Box2D.b2PolygonDef()
        shapeDef.SetAsBox(width / 2.0 /  PIXELS_PER_METER, height / 2.0 / PIXELS_PER_METER)
        if isStatic:
            shapeDef.density = 0
        else:
            shapeDef.density = DENSITY
        shapeDef.friction = FRICTION
        
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()

    def update(self):
        '''
        Overrides Sprite update
        '''

        if Viewport().hasMoved:
            self.rect.center = Viewport().convertPhysicalToPixelCoords(self._physicalPosition)
            self.dirty = 1
            
        if self.hasPhysics:
            print "Passing in:",self.body.position.x,self.body.position.y
            newPhysicalPosition = Vect(self.body.position.x,self.body.position.y)
            if newPhysicalPosition != self.physicalPosition:
                self._setPhysicalPosition(newPhysicalPosition)

    def _setPhysicalPosition(self,value):
        try:
            print "oldPos",self._physicalPosition,"New Pos: ",value    
        except:
            pass
        self._physicalPosition = Vect(value[0],value[1])
        
        self.rect.center = Viewport().convertPhysicalToPixelCoords(value)
        self.dirty = 1

    def _getPhysicalPosition(self):
        return self._physicalPosition

    physicalPosition = property(_getPhysicalPosition,_setPhysicalPosition)
    
    def _setPixelPosition(self,value):
        self.rect.move_ip(*value)
        self._physicalPosition = Viewport().convertPixelsToPhysicalCoords(self.rect.center)

    def _getPixelPosition(self):
        return (self.rect.left,self.rect.top)

    pixelPosition = property(_getPixelPosition,_setPixelPosition)

class Crate(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="crate"):
        RenderableObject.__init__(self,position,physicsWorld,imageName)

class RoomBg(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="roombg"):
        RenderableObject.__init__(self,position,physicsWorld,imageName,hasPhysics=False)

class Platform(RenderableObject):
    def __init__(self,position,physicsWorld,imageName="simplePlatform"):
        RenderableObject.__init__(self,position,physicsWorld,imageName,hasPhysics=True,isStatic=True,canRotate=False)

class Spaceman(RenderableObject):
    def __init__(self,position,physicsWorld):
        pygame.sprite.DirtySprite.__init__(self)
        self.spriteSheetRight = ImageHandler()["walkingRight"] # Returns a pygame surface
        self.spriteSheetLeft = ImageHandler()["walkingLeft"] # Returns a pygame surface
        
        sprite_height = 90
        sprite_width = 80

        self.rect = pygame.Rect(0,0,sprite_width,sprite_height)

        if not isinstance(position, Vect):
            physicalPosition = Vect(*position)
        self.physicalPosition = position

        self.physicsWorld = physicsWorld

        self.spritesRight = list()
        self.spritesLeft  = list()

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

        self.spriteIndex = 0
        self.image = self.spritesRight[self.spriteIndex]

        self.hasPhysics = True
        self._buildPhysics(width=sprite_width,height=sprite_height,canRotate=True,isStatic=False)

        
    def update(self):
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

    def tryMove(self, x, y):
        print "foobar"
        print self.physicalPosition

        print "Get World Center",self.body.GetWorldCenter()

        #self.body.ApplyForce(Box2D.b2Vec2(600,0),self.body.GetWorldCenter())
        self.body.ApplyForce(Box2D.b2Vec2(600,0),Box2D.b2Vec2(self.physicalPosition[0],self.physicalPosition[1]))

        return
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
