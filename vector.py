import math
import random
class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return str(self.x) + ' , ' + str(self.y) + ' , ' + str(self.z)

    def __repr__(self):
        return str(self.x) + ' , ' + str(self.y) + ' , ' + str(self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    # Add any two vectors together : returns a vector
    def __add__(self, other):
        x1 = self.x
        y1 = self.y
        z1 = self.z
        x2 = other.x
        y2 = other.y
        z2 = other.z
        return Vector(x1+x2, y1+y2, z1 + z2)

    # Subtract any two vectors  : returns a vector
    def __sub__(self, other):
        x1 = self.x
        y1 = self.y
        z1 = self.z
        x2 = other.x
        y2 = other.y
        z2 = other.z
        return Vector((x1 - x2), (y1 - y2), (z1 - z2))

    # Multiply a vector by a number
    def __mul__(self, other):
        x1 = self.x
        y1 = self.y
        z1 = self.z
        return Vector(x1*other, y1*other, z1*other)

    def __rmul__(self, other):
        return self.__mul__(other)

    # absoulute value/magnitude
    def __abs__(self):
        return self.mag()

    # magnitude of the vector
    def mag(self):
        expression = self.x**2 + self.y**2 + self.z**2
        return math.sqrt(expression)

    # Take the dot product
    def dot(self, other):
        x, y, z = other.x, other.y, other.z
        return self.x * x + self.y * y + self.z * z

    # Makes all values 1
    def normalize(self):
        signX = 1 if self.x > 0 else -1
        signY = 1 if self.y > 0 else -1
        signZ = 1 if self.z > 0 else -1
        self.x = 1*signX if self.x != 0 else 0
        self.y = 1*signY if self.y != 0 else 0
        self.z = 1*signZ if self.z != 0 else 0

    # Sets the value of a vector to the one desired
    def setMag(self, mag):
        self.normalize()
        self.x *= mag
        self.y *= mag
        self.z *= mag
        return Vector(self.x, self.y, self.z)

    # Take the cross product of two vectors
    def cross(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x
        return Vector(x, y, z)

    # Limit the value of the vector
    def limit(self, maximum):
        if self.mag() > maximum:
            self.setMag(maximum)

    # Get the distance between two vectors
    def dist(self, other):
        x1 = self.x
        y1 = self.y
        z1 = self.z
        x2 = other.x
        y2 = other.y
        z2 = other.z
        expression = (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
        return math.sqrt(expression)
    # Get the angle from the x-axis
    @staticmethod
    def heading(vector):
        h = math.atan2(vector.y, vector.x)
        return h

    # Make vector from angle with desired magnitude
    @staticmethod
    def fromAngle(angle):
        desiredVector = Vector(math.cos(angle), math.sin(angle))
        return desiredVector
    # Get a random vector
    @staticmethod
    def randomVector():
        angle = random.uniform(0, 2*math.pi)
        return Vector.fromAngle(angle) *2
