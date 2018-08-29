from vector import *
import random

class Projectile(object):
    def __init__(self, start, destination, color='blue'):
        # Where the projectile spawns
        self.location = start
        # The color of the projectile
        self.color = color
        self.destination = destination - start
        heading = Vector.heading(self.destination)
        vectorFromAngle = Vector.fromAngle(heading)
        vectorFromAngle *= 10

        # # The destination
        # self.direction = vectorFromAngle
       # The velocity of the projectile
        self.velocity = vectorFromAngle
        self.size = 20
        self.path = []


    def __str__(self):
        return str(self.location) + ' with velocity ' + str(self.velocity)

    def __repr__(self):
        return self.__str__()

    # Apply a given force to the projectile
    def applyForce(self, steering):
        self.location += steering
        self.path.append(self.location)
        if len(self.path) > 5:
            self.path.pop(0)

    # Seek ( go towards ) a given point
    def seek(self):
        self.applyForce(self.velocity)
    # Draw it
    def draw(self, canvas):
        initalR = self.size//6
        for i in range(0, len(self.path)):
            currLoc = self.path[i]
            canvas.create_oval(currLoc.x - initalR*i/2, currLoc.y - initalR*i/2,
                               currLoc.x  + initalR*i/2,
                               currLoc.y + initalR* i/2, fill=self.color)




    def isOffScreen(self, data):
        x, y = self.location.x, self.location.y
        return x <= 0 or x >= data.width or y <= 0 or y >= data.height

    def collisionWith(self, other):
        x, y = self.location.x, self.location.y
        otherX, otherY = other.location.x, other.location.y
        return otherX - other.size - 10 < x < otherX + other.size + 10 and \
               otherY - other.size - 10 < y < otherY + other.size + 10
