from __future__ import division
from visual import *
from math import pi,cos,sin
from random import random
from time import sleep
from threading import Thread, RLock
import simpleParser
import treeMap
import sys


ox = vector(1,0,0)
oy = vector(0,1,0)
oz = vector(0,0,1)


class Tree(object):
    def __init__(self, father, content):
        self.father = None
        self.content = content
        self.children = []
        if not father:
            self.height = 0
        self.setFather(father)

    def append(self, children):
        self.children.append(children)

    def __str__(self):
        if self.children:
            return '[%s, %s]' % (self.content,
                                 ', '.join(str(child) for child in self))
        else:
            return '[%s]' % self.content

    def size(self):
        if len(self.children) == 0:
            return 1
        else:
            return sum(size(child) for child in self)

    def index(self):
        if self.father == None:
            return 0
        else:
            return self.father.children.index(self)

    def setFather(self, father):
        if self == father:
            return
        if self.father:
            self.father.children.remove(self)
        self.father = father
        if self.father:
            self.father.children.append(self)
            self.height = self.father.height + 1
            for child in self:
                child.setFather(self)

    def setFatherAtIndex(self, father, index):
        if self == father:
            return
        if self.father:
            self.father.children.remove(self)
        self.father = father
        if self.father:
            self.father.children.insert(index, self)
            self.height = self.father.height + 1
            for child in self:
                child.setFather(self)

    def remove(self):
        index = self.index()
        for child in self:
            child.setFatherAtIndex(self.father, index)
            index += 1
        self.setFather(None)

    def __iter__(self):
        return iter(list(self.children))


class Planet(object):
    def __init__(self, node, color):
        self.node = node
        self._removed = False
        self._removed_timer = 200

        if not node.father:
            self.sphere = sphere(pos=(0, 0, 0), radius=0.5, color=color)
        else:
            self._theta = random() * pi
            self._phi = random() * pi
            self._psi = random() * pi

            self.sphere = sphere(pos=(0, 0, 0), radius=0, color=color)

            self._moving = True
            self._moving_timer = 1000
            self.update()
            self.placeSphere()

    def color(self):
        return self.sphere.color;

    def placeSphere(self):
        position = self.position()
        if (not self._moving) or self._moving_timer == 0:
            self._moving = False
            self.sphere.pos = position
            self.sphere.radius = self.radius
        else:
            mt = self._moving_timer
            self.sphere.pos = (1 - 5/mt) * self.sphere.pos + 5/mt * position
            self.sphere.radius = (1 - 5/mt) * self.sphere.radius + 5/mt * self.radius
            self._moving_timer -= 1

    def position(self):
        positionFather = self.node.father.content.sphere.pos
        position = positionFather + self.radius * 8 * (
                (sin(self._psi) * cos(self._theta) + cos(self._psi) * sin(self._phi) * sin(self._theta) ) * ox +
                (sin(self._psi) * sin(self._theta) - cos(self._psi) * sin(self._phi) * cos(self._theta) ) * oy +
                (cos(self._psi) * cos(self._phi)) * oz)

        return position

    def tick(self):
        if self.node.father:
            self._psi += self.angularVelocity
            self.placeSphere()
        elif self._removed:
            self.tickRemove()

    def remove(self):
        l = list(self.node.children)
        self.node.remove()
        for child in l:
            child.content.update()
        self._removed = True

    def tickRemove(self):
        self.sphere.radius = (1 - 1/self._removed_timer) * self.sphere.radius
        self._removed_timer -= 1
        if self._removed_timer == 0:
            self.sphere.visible = False
            del self.sphere
            planetList.remove(self)

    def append(self, color):
        node = Tree(self.node, None)
        node.content = Planet(node, color)
        planetList.append(node.content)
        return node.content

    def update(self):
        height = self.node.height
        self.radius = 1/4**height
        self.angularVelocity = height * 2 * pi/500
        self._moving_timer = 200
        self._moving = True


planetList = []


if __name__ == '__main__':
    source = sys.argv[1]

    print source

    def buildPlanets(tree):
        tree.content = Planet(tree, tree.content)
        planetList.append(tree.content)
        for child in tree:
            buildPlanets(child)

    res = simpleParser.parse(source)
    tree = simpleParser.createTreeFromParse(res, (1, 1, 1), None)

    buildPlanets(tree)
    count = 0
    while True:
        for planet in planetList:
            planet.tick()
        rate(100)

        if count >= 20:
            try:
                res = simpleParser.parse(source)
                tree = simpleParser.createTreeFromParse(res, (1, 1, 1), None)

                treeMap.planetMap(planetList[0], tree)
            except IOError:
                pass
            count = 0
        else:
            count += 1
