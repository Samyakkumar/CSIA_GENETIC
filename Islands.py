import random
from pynoise.noisemodule import Perlin
from vector import Vector
import math
import os
from Organisms import Tree
from Organisms import Animal

os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'

class Islands(object):
    def __init__(self, bounds, title, type, flameImages):
        self.perlin = Perlin()
        self.pointsIsland = []
        self.title = title
        self.organisms = []
        self.organismType = type
        self.numOrganisms = 100
        self.xBound = bounds[0]
        self.yBound = bounds[1]
        self.organismSize = 4
        self.extinct = set()
        self.callCheck = False
        self.flameImages = flameImages
        print(self.flameImages)

    @staticmethod
    def getFrequencies(organisms):
        result = dict()
        for organism in organisms:
            if organism.alleles not in result:
                result[organism.alleles] = [1, organism.col]
            elif organism.alleles in result:
                result[organism.alleles][0] += 1
        return result

    def makePointsIslands(self):
        startAngle = 0
        xoff = random.randint(0, 100)
        while startAngle < 2 * math.pi:
            currVector = Vector.fromAngle(startAngle)
            currVector *= 170
            randVect = Vector(self.translate(self.perlin.get_value(xoff, 0, 0), 0, 1, -20, 20))
            newVect = currVector + randVect
            self.pointsIsland.append(newVect)
            startAngle += 0.1
            xoff += 0.1
    
            
    def checkOrganisms(self, removeAllele):
        for organism in self.organisms:
            if not organism.isAlive:
                self.organisms.remove(organism)
        if len(self.organisms) > self.numOrganisms:
            self.organisms = self.organisms[:self.numOrganisms]
        elif len(self.organisms) < self.numOrganisms:
            for i in range(self.numOrganisms - len(self.organisms)):
                self.addOneTree(removeAllele)
#         print('after checking', len(self.organisms))

    def showIsland(self, canvas):
        self.canvas = canvas
        pointsTuple = ()
        cx, cy = self.xBound, self.yBound
        for point in self.pointsIsland:
            pointsTuple += ((cx + point.x, cy - point.y),)
        canvas.create_polygon(pointsTuple, fill='pale green')
        canvas.create_text(cx - 10, cy - 155, text=self.title, font=("Helvetica", '19'))

    # taken https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
    def translate(self,value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def addOrganisms(self):
        if self.organismType == 'Tree':
            alleles = [('Tt'), ("TT"), ('tt')]
            self.addTrees(random.choice(alleles))
        elif self.organismType == 'Animal':
            alleles = [('Tt'), ("TT")]
            self.addAnimals(random.choice(alleles))
        print("ADDED ORGANISMS")


    def addTrees(self, alleles):
        startAngle = random.uniform(0, 2*math.pi)
        r = self.organismSize
        cx, cy = self.xBound, self.yBound
        for i in range(self.numOrganisms):
            alleles = [('Tt'), ("TT"), ('tt')]
            alleles = random.choice(alleles)
            multiplier = random.randint(-1, 28)
            self.organisms.append(Tree(True, alleles, Vector(cx + math.cos(startAngle) * r * multiplier,
                                                             cy + math.sin(startAngle)* r * multiplier), alleles, self.organismSize, self.flameImages))
            startAngle += random.uniform(0, 1)
        
    def addOneTree(self, alleles=[('Tt'), ("TT"), ('tt')]):
#         print("pop", self.title)
#         print('extinct', self.extinct)
        for i in alleles:
            if i in self.extinct:
                alleles.remove(i)
        startAngle = random.uniform(0, 2*math.pi)
        if alleles != [('Tt'), ("TT"), ('tt')]:
            if isinstance(alleles, list):
                alleles = random.choice(alleles)
            else:
                alleles = random.choice([alleles, alleles])
        else:
            alleles = random.choice([('Tt'), ("TT"), ('tt')])
            print(alleles)
        
        print('added', alleles)
        r = self.organismSize
        cx, cy = self.xBound, self.yBound
        multiplier = random.randint(-1, 28)
        self.organisms.append(Tree(True, alleles, Vector(cx + math.cos(startAngle) * r * multiplier,
                                                             cy + math.sin(startAngle)* r * multiplier), alleles, self.organismSize, self.flameImages))

    def addAnimals(self, alleles):
        startAngle = random.uniform(0, 2 * math.pi)
        r = self.organismSize
        cx, cy = self.xBound, self.yBound
        for i in range(self.numOrganisms):
            multiplier = random.randint(-1, 28)
            self.organisms.append(Animal(True, alleles, Vector(cx + math.cos(startAngle) * r * multiplier,
                                                             cy + math.sin(startAngle) * r * multiplier)))
            startAngle += 0.1
            alleles = [('Tt'), ("TT")]
            alleles = random.choice(alleles)

    def showOrganisms(self, canvas):
        for organism in self.organisms:
            organism.show(canvas)
        