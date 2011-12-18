#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import pygame
from pygame.locals import *
from Box2D import *

from globals import *

class ViewPort(object):
    #implement a singleton pattern here...
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ViewPort, cls).__new__(cls, *args, **kwargs)
        return cls._instance
    
    def __init__(self):
        x_offset = Dimension(unitstr='0 m')
        y_offset = Dimension(value=SCREEN_REAL_HEIGHT, units={"m": 1})
        self.originDelta = Vect(x_offset, y_offset)

    def ScreenCoords(self, physxCoords):
        physxCoords = physxCoords.ConvertTo(Dimension(value=1.0, units={'m': 1}))
        px = physxCoords.x
        py = physxCoords.y
        dx = self.originDelta.x
        dy = self.originDelta.y
        x = px - dx
        y = dy - py
        screenCoords = Vect(x, y)
        return screenCoords.ConvertTo(Dimension(value=1.0, units={'px': 1}))


class World(b2World):
    def __init__(self, size, gravity):
        self.size = size # [m]
        self.drawables = []
        world = b2AABB()
        world.lowerBound = (0, 0)
        world.upperBound = size.ConvertTo(Dimension(unitstr="1.0 m")).Strip()
        doSleep = True
        super(World, self).__init__(world, gravity, doSleep)


class Rect(object):
    def __init__(self, world, pos, size, density):
        bodyDef = b2BodyDef()
        bodyDef.position = pos.ConvertTo(Dimension(unitstr="1.0 m")).Strip()
        self.body = world.CreateBody(bodyDef)
        world.drawables.append(self)
        self.vp = ViewPort()

        shapeDef = b2PolygonDef()
        shapeDef.SetAsBox(*(size / 2.0).ConvertTo(
            Dimension(unitstr="1.0 m")).Strip())
        shapeDef.density = density
        shapeDef.linearDamping = AIR_RESISTANCE
        shapeDef.friction = FRICTION
        
        self.body.CreateShape(shapeDef)
        self.body.SetMassFromShapes()
        
        self.size = size
        self.pos = pos

    def posVect(self):
        xr = self.body.position.x
        yr = self.body.position.y
        x = Dimension(value=xr, units={'m': 1})
        y = Dimension(value=yr, units={'m': 1})
        return Vect(x, y)

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

    def draw(self, surface):
        corners = self.GetCorners()
        for i in range(len(corners) + 1):
            pos_start = self.vp.ScreenCoords(corners[i - 2]).Strip()
            pos_end = self.vp.ScreenCoords(corners[i - 1]).Strip()
            pygame.draw.line(surface, (255, 255, 255), pos_start, pos_end, 2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((1024, 768))

    background = pygame.Surface(screen.get_size())
    background = background.convert()

    clock = pygame.time.Clock()
    
    screen_width = SCREEN_REAL_WIDTH * METER
    screen_height = SCREEN_REAL_HEIGHT * METER
    w = World(Vect(screen_width, screen_height), GRAVITY)
    vp = ViewPort()
    
    groundRectPos = Vect(screen_width / 2.0, 0.5 * METER)
    groundRectSize = Vect(screen_width, 1.0 * METER)
    groundRect = Rect(w, groundRectPos, groundRectSize, 0)

    rect1 = Rect(w, Vect(9.0 * METER, 9.0 * METER), Vect(METER, METER), 1)
    rect2 = Rect(w, Vect(10.0 * METER, 18.0 * METER), Vect(METER * 2, METER), 1)

    while True:
        tstep = clock.tick(30)
        background.fill((0, 0, 0))
        for body in w.drawables:
            body.draw(background)
        screen.blit(background, (0, 0))
        pygame.display.flip()
        w.Step(tstep / 1000.0, 10, 8)
        for event in pygame.event.get():
            if event.type == QUIT:
                return


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
