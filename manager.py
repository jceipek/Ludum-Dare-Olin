#!/usr/bin/python
# -*- coding: us-ascii -*-

import sys
import pygame
import math
import fractions
import numbers
from pygame.locals import *
from Box2D import *

from globals import *

class Vect(object):
    def __init__(self, x, y):
        x.CheckUnits(y)
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vect(other * self.x, other * self.y)

    def __rmul__(self, other):
        return Vect(self.x * other, self.y * other)

    def __div__(self, other):
        return Vect(self.x / other, self.y / other)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def Canonicalize(self):
        self.x.Canonicalize()
        self.y.Canonicalize()

    def ConvertTo(self, target):
        return Vect(self.x.ConvertTo(target), self.y.ConvertTo(target))

    def Strip(self):
        return (self.x.Strip(), self.y.Strip())

    def Rotate(self, theta):
        x, y = self.x, self.y
        newx = x * math.cos(theta) - y * math.sin(theta)
        newy = x * math.sin(theta) + y * math.cos(theta)
        self.x = newx
        self.y = newy

    def MirrorH(self):
        return Vect(-self.x, self.y)

    def MirrorV(self):
        return Vect(self.x, -self.y)

    def __str__(self):
        return '<%s, %s>' % (self.x, self.y)

class Dimension(object):
    base_units = ('m', 'kg', 's')
    alt_units = {'px': (1 / PIXELS_PER_METER, 'm')}
    def __init__(self, value=None, units=None, unitstr=None):
        if unitstr != None:
            value, sp, unitstr = unitstr.partition(' ')
            self.value = float(value)
            self.MakeDict(unitstr)
        else:
            self.value = value
            self.units = {}
            for key in units:
                self.units[key] = units[key]

    def MakeDict(self, unitstr):
        self.units = {}
        for unitspec in unitstr.split(' '):
            if '^' not in unitspec:
                unit = unitspec
                exp = "1"
            else:
                unit, exp = unitspec.split('^')
            
            if unit in self.units.keys():
                self.units[unit] += fractions.Fraction(exp)
            else:
                self.units[unit] = fractions.Fraction(exp)
            
            if self.units[unit] == 0:
                del self.units[unit]

    def CopyDict(self):
        dict = {}
        for key in self.units.keys():
            dict[key] = self.units[key]
        return dict

    def Canonicalize(self):
        for unit in self.units:
            if unit in self.alt_units.keys():
                factor, target = self.alt_units[unit]
                exp = self.units[unit]
                self.value *= math.pow(factor, exp)
                del self.units[unit]
                self.units[target] = exp

    def ConvertTo(self, target):
        newself = Dimension(value=self.value, units=self.CopyDict())
        newtarget = Dimension(value=target.value, units=target.CopyDict())
        newself.Canonicalize()
        newtarget.Canonicalize()
        value = newself.value/newtarget.value
        return Dimension(value=value, units=target.units)

    def Strip(self):
        return float(self.value)

    def CheckUnits(self, other):
        if self.units != other.units:
            raise ValueError("Incompatible Dimensions")
    
    def DeepCopy(self):
        newself = Dimension(value=self.value, units=self.CopyDict())
        return newself

    def CheckDimensions(self, other):
        newself = self.DeepCopy()
        newother = self.DeepCopy()
        newself.Canonicalize()
        newother.Canonicalize()
        newself.CheckUnits(newother)

    def __add__(self, other):
        self.CheckUnits(other)
        return Dimension(value=(self.value + other.value), units=self.units)

    def __sub__(self, other):
        self.CheckUnits(other)
        return Dimension(value=(self.value - other.value), units=self.units)

    def __neg__(self):
        return Dimension(value=(-self.value), units=self.units)

    def __mul__(self, other):
        if isinstance(other, numbers.Number):
            value = self.value * other
            units = self.units
        else:
            value = self.value * other.value
            units = {}
            for unit in self.units.keys():
                units[unit] = self.units[unit]
            for unit in other.units.keys():
                if unit in units.keys():
                    units[unit] += other.units[unit]
                else:
                    units[unit] = other.units[unit]
            for unit in units.keys():
                if units[unit] == 0:
                    del units[unit]
        return Dimension(value=value, units=units)
    
    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, numbers.Number):
            return self * (1/other)
        return other.Reciprocal() * self

    def __div__(self, other):
        return self.__truediv__(other)

    def __rtruediv__(self, other):
        return other * self.Reciprocal()

    def __rdiv__(self, other):
        return self.__rtruediv__(other)

    def Reciprocal(self):
        recip = {}
        for unit in self.units.keys():
            recip[unit] = -self.units[unit]
        return Dimension(value=(1.0/self.value), units=recip)

    def __str__(self):
        outstr = str(self.value) + ' '
        return outstr + self.GetUnitStr()

    def GetUnitStr(self):
        outstr = ''
        for unit in sorted(self.units.keys()):
            outstr += unit
            exp = self.units[unit]
            n = exp.numerator
            d = exp.denominator
            if d != 1 or n != 1:
                outstr += '^' + str(n)
                if d != 1:
                    outstr += '/' + str(d)
            outstr += ' '
        return outstr[:-1]
                
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
    
    screen_width = Dimension(value=SCREEN_REAL_WIDTH, units={'m': 1})
    screen_height = Dimension(value=SCREEN_REAL_HEIGHT, units={'m': 1})
    w = World(Vect(screen_width, screen_height), GRAVITY)
    vp = ViewPort()
    
    meter = Dimension(value=1.0, units={'m': 1})
    
    groundRectPos = Vect(screen_width / 2.0, 0.5 * meter)
    groundRectSize = Vect(screen_width, 1.0 * meter)
    groundRect = Rect(w, groundRectPos, groundRectSize, 0)

    rect1 = Rect(w, Vect(9.0 * meter, 9.0 * meter), Vect(meter, meter), 1)
    rect2 = Rect(w, Vect(10.0 * meter, 18.0 * meter), Vect(meter * 2, meter), 1)

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
