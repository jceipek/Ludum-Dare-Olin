#!/usr/bin/python
# -*- coding:us-ascii -*-

import sys
import time
from Box2D import *

worldAABB=b2AABB()
worldAABB.lowerBound.Set(-100, -100)
worldAABB.upperBound.Set(100, 100)

worldAABB=b2AABB()
worldAABB.lowerBound = (-100, -100)
worldAABB.upperBound = (100, 100)

gravity = (0, -0.1) # for pybox2d < 2.0.2b1, this must be a b2Vec2
doSleep = True

world = b2World(worldAABB, gravity, doSleep)

groundBodyDef = b2BodyDef()
groundBodyDef.position = (0, -10)

groundBody = world.CreateBody(groundBodyDef)

groundShapeDef = b2PolygonDef()
groundShapeDef.SetAsBox(50, 10)

groundBody.CreateShape(groundShapeDef)


for i in range(100):
    bodyDef = b2BodyDef()
    bodyDef.position = (i*1.01, 100)
    body = world.CreateBody(bodyDef)

    shapeDef = b2PolygonDef()
    shapeDef.SetAsBox(0.5, 0.5)
    shapeDef.density = 1
    shapeDef.friction = 0.3
    body.CreateShape(shapeDef)
    body.SetMassFromShapes()

print body

timeStep = 1.0 / 600.0

velocityIterations = 10
positionIterations = 8

world.Step(timeStep, velocityIterations, positionIterations)

start1 = time.time()
i = 0.0
for i in range(6000):
    i += 0.05
    world.Step(timeStep, velocityIterations, positionIterations)
print time.time() - start1
print body.position.y

body.position = b2Vec2(0, 100)
body.linearVelocity = b2Vec2(0, 0)
start2 = time.time()
i = 0.0
for i in range(6000):
    i += 0.05
    world.gravity = (0, -0.1)
    world.Step(timeStep, velocityIterations, positionIterations)
print time.time() - start2
print body.position.y


