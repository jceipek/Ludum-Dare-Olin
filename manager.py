#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import pygame
import math
from pygame.locals import *
from Box2D import *
import dimension

from globals import *

class ViewPort(object):
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ViewPort, cls).__new__(cls, *args, **kwargs)
            self = cls._instance
            print "Creating ViewPort Singleton"
            x_offset = 0 * METER
            y_offset = SCREEN_REAL_HEIGHT * METER
            self.originDelta = dimension.Vect(x_offset, y_offset)

        return cls._instance

    def ScreenCoords(self, physxCoords):
        physxCoords = physxCoords.ConvertTo(METER)
        self.originDelta = self.originDelta.ConvertTo(METER)
        px = physxCoords.x
        py = physxCoords.y
        dx = self.originDelta.x
        dy = self.originDelta.y
        x = px - dx
        y = dy - py
        screenCoords = dimension.Vect(x, y)
        return screenCoords.ConvertTo(PIXEL)
    
    def PhysxCoords(self, screenCoords):
        screenCoords = screenCoords.ConvertTo(METER)
        self.originDelta = self.originDelta.ConvertTo(METER)
        sx = screenCoords.x
        sy = screenCoords.y
        dx = self.originDelta.x
        dy = self.originDelta.y
        px = sx + dx
        py = dy - sy
        physxcoords = dimension.Vect(px,py)
        return physxcoords


class World(b2World):
    def __init__(self, size, gravity):
        self.size = size # [m]
        self.drawables = []
        world = b2AABB()
        world.lowerBound = (0, 0)
        world.upperBound = size.ConvertTo(METER).Strip()
        doSleep = False
        super(World, self).__init__(world, gravity, doSleep)
        self.points=[]
        

class Rect(object):
    def __init__(self, world, pos, size, density, groupIndex=0):
        bodyDef = b2BodyDef()
        bodyDef.position = pos.ConvertTo(METER).Strip()
        self.body = world.CreateBody(bodyDef)
        world.drawables.append(self)
        self.vp = ViewPort()

        shapeDef = b2PolygonDef()
        shapeDef.SetAsBox(*(size / 2.0).ConvertTo(METER).Strip())
        shapeDef.density = density
        shapeDef.linearDamping = AIR_RESISTANCE
        shapeDef.friction = FRICTION
        shapeDef.restitution = 0.3
        shapeDef.filter.groupIndex = groupIndex
        
        self.shape = self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()
        
        self.size = size
        self.pos = pos

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

    def blitToScreen(self, surface):
        corners = self.GetCorners()
        for i in range(len(corners) + 1):
            pos_start = self.vp.ScreenCoords(corners[i - 2]).Strip()
            pos_end = self.vp.ScreenCoords(corners[i - 1]).Strip()
            pygame.draw.line(surface, (255, 255, 255), pos_start, pos_end, 2)


def kickMagnitude(tminus):
    t = float(FRAMERATE - tminus) / float(FRAMERATE)
    a = 2.0
    b = 0.5
    c = 0.33
    return math.exp(-((t - b)**2) / (2 * c**2))

class ChainBody(object):
    def __init__(self, bodies):
        self.bodies = bodies

    def WakeUp(self):
        for body in self.bodies:
            body.WakeUp()

class Chain(object):
    def __init__(self, world, startpos, length, anchor):
        #world.drawables.append(self)
        resolution = 10
        width = 0.1 * METER
        self.vp = ViewPort()
        self.shapes = []
        self.bodies = []
        self.rects = []
        self.pins = []
        
        unit = dimension.Vect(0 * METER, -length / float(resolution))
        prevBody = anchor
        for i in range(resolution):
            anchor0 = startpos + (unit * i)
            anchor1 = anchor0 + unit
            center = (anchor0 + anchor1) / 2.0
            size = dimension.Vect(width, -unit.y + 2 * width)
            #bodyDef = b2BodyDef()
            #bodyDef.position = center.Strip()
            #body = world.CreateBody(bodyDef)
            #shapeDef = b2PolygonDef()
            #shapeDef.SetAsBox((width/2).Strip(), (size/2).Strip())
            #shapeDef.density = 1
            #shapeDef.linearDamping = AIR_RESISTANCE
            #shape = body.CreateShape(shapeDef)
            #self.shapes.append(shape)
            #self.bodies.append(body)
            rect = Rect(world, center, size, 1, groupIndex=-1)
            world.drawables.append(rect)
            self.rects.append(rect)
            body = rect.body
            self.bodies.append(body)
            self.pins.append(anchor0)

            jointDef = b2RevoluteJointDef()
            jointDef.Initialize(prevBody, body, anchor0.Strip())
            print anchor0
            world.CreateJoint(jointDef)
            prevBody = body

    def blitToScreen(self, surface):
        #for i in range(len(self.pins)):
        #    pos_start = self.vp.ScreenCoords(self.pins[i - 1]).Strip()
        #    pos_end = self.vp.ScreenCoords(self.pins[i]).Strip()
        #    pygame.draw.line(surface, (255, 255, 255), pos_start, pos_end, 2)
        for pin in self.pins:
            pos = self.vp.ScreenCoords(pin).Strip()
            surface.set_at(pos, (255, 0, 0))

def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))

    background = pygame.Surface(screen.get_size())
    background = background.convert()

    clock = pygame.time.Clock()
    
    screen_width = SCREEN_REAL_WIDTH * METER
    screen_height = SCREEN_REAL_HEIGHT * METER
    w = World(dimension.Vect(screen_width, screen_height), GRAVITY)
    vp = ViewPort()
    
    groundRectPos = dimension.Vect(screen_width / 2.0, 0.5 * METER)
    groundRectSize = dimension.Vect(screen_width, 1.0 * METER)
    groundRect = Rect(w, groundRectPos, groundRectSize, 0)

    ceilingRectPos = dimension.Vect(screen_width / 2.0, screen_height - 0.5 *
                                    METER)
    ceilingRectSize = dimension.Vect(screen_width, 1.0 * METER)
    ceilingRect = Rect(w, ceilingRectPos, ceilingRectSize, 0)
    
    ch = Chain(w, ceilingRectPos, 10 * METER, ceilingRect.body)
    
    rect1pos = dimension.Vect(12.8 * METER, 8.7 * METER)
    rect1 = Rect(w, dimension.Vect(12.8 * METER, 8.7 * METER), 
                 dimension.Vect(1 * METER, METER), 1, groupIndex=-1)
    jointDef = b2RevoluteJointDef()
    jointDef.Initialize(ch.bodies[-1], rect1.body, rect1pos.Strip())
    w.CreateJoint(jointDef)
    #rect2 = Rect(w, dimension.Vect(9.0 * METER, 4.0 * METER), 
    #             dimension.Vect(METER * 9.0, METER), 1)
    #rect3 = Rect(w, dimension.Vect(5.5 * METER, 5.0 * METER),
    #             dimension.Vect(METER * 0.2, METER * 0.2), 0.2)
    #rect4 = Rect(w, dimension.Vect(METER * 13.0, 9.0 * METER), 
    #             dimension.Vect(METER, METER), 1)

    
    kickcount = 0
    while True:
        tstep = clock.tick(FRAMERATE)
        if kickcount > 1:
            kick = kickd * kickMagnitude(kickcount)
            gravity = dimension.Vect(0 * METER, -10 * METER) + kick
            # print gravity
            w.gravity = gravity.Strip()
            kickcount -= 1
            for rect in w.drawables:
                rect.body.WakeUp()
        elif kickcount > 0:
            w.gravity = GRAVITY
            kickcount -= 1
        background.fill((0, 0, 0))
        for body in w.drawables:
            body.blitToScreen(background)
        screen.blit(background, (0, 0))
        pygame.display.flip()
        w.Step(tstep / (1000.0), 10, 8)
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    kickcount = 1.0 * FRAMERATE
                    kickd = dimension.Vect(-1 * METER, 0 * METER) * 3
                if event.key == pygame.K_k:
                    kickcount = 1.0 * FRAMERATE
                    kickd = dimension.Vect(0 * METER, 1 * METER) * 15
                if event.key == pygame.K_l:
                    kickcount = 1.0 * FRAMERATE
                    kickd = dimension.Vect(1 * METER, 0 * METER) * 3
                if event.key == pygame.K_i:
                    kickcount = 1.0 * FRAMERATE
                    kickd = dimension.Vect(0 * METER, -1 * METER) * 15
                if event.key == pygame.K_w:
                    rect1.body.ApplyForce((0, 150), rect1.body.position)

def unittest():
    x1 = Dimension(unitstr='160 px')
    y1 = Dimension(unitstr='120 px')
    x2 = Dimension(unitstr='32 px')
    y2 = Dimension(unitstr='32 px')
    v1 = Vect(x1, y1)
    v2 = Vect(x2, y2)
    print v1
    print v2
    print v1 + v2
    print v1 - v2
    print 3.0 * v1
    print v2 / 1.875
    v1.Canonicalize()
    print v1
    print v2.ConvertTo(Dimension(unitstr='1.0 m'))
    print v2
    v2.Rotate(45 * math.radians(45))
    print v2


if __name__ == '__main__':
    sys.exit(main())
