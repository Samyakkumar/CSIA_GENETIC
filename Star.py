from vector import Vector
import random
class Star(object):
    def __init__(self, data, vel, color=None):
        self.r = 2
        self.location = Vector(random.randint(-data.width//2, data.width),
            random.randint(-data.height//2, data.height))
        self.vel = vel
        self.z = random.randint(1, data.width)
        self.previousZ = self.z
        self.data = data
        self.color = color if color else 'white'

    def draw(self, canvas):
        x, y = self.location.x, self.location.y

        if self.z > 0:
            sx = self.translate(x / self.z, 0, 1, self.data.width // 2,
            self.data.width)
            sy = self.translate(y / self.z, 0, 1, self.data.height // 2,
             self.data.height)
            r = self.translate(self.z, 0, self.data.width, 5, 0)
            previousX = self.translate(x / self.previousZ, 0, 1,
                self.data.width // 2, self.data.width)
            previousY = self.translate(y / self.previousZ, 0, 1,
                self.data.height // 2, self.data.height)

            self.previousZ = self.z
            canvas.create_line(previousX, previousY, sx, sy, fill=self.color, width=2.0)
    def move(self):
        self.z -= 25

    def translate(self,value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def offScreen(self):
        if self.z <= 0:
            self.location = Vector(random.randint(-self.data.width,
            self.data.width),
                                   random.randint(-self.data.height,
                                   self.data.height))
            self.z = self.data.width
            self.previousZ = self.z
