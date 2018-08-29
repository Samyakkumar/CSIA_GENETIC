import random

class Organisms(object):
    def __init__(self, isAlive, alleles, points, position, col, fireImage=None):
        self.isAlive = isAlive
        self.alleles = alleles
        print(self.alleles)
        self.points = points
        self.position = position
        self.col = col
        self.fireImage = fireImage

    def show(self, canvas):
        canvas.create_oval(self.position.x - 5, self.position.y - 5,
                           self.position.x + 5, self.position.y + 5, fill=self.col)



class Tree(Organisms):
    def __init__(self, isAlive, alleles, position, color, size, fireImage):
        self.isAlive = isAlive
        self.alleles = alleles
        self.position = position
        self.possibleCols = {'Tt':'green', 'tt':'sea green', 'TT':'dark green', 'TR':'red', 'tR':'red', 'TB' : 'brown', 'tB':'brown'}
        self.col = self.possibleCols[color]
        self.size = size
        self.startSize = 0
        self.makeSmaller = False
        self.grow = True
        self.fireImage = fireImage

#     def getRandomColor(self):
#         return random.choice(self.possibleCols)

    def show(self, canvas):
        if self.isAlive and not self.grow:
            size = self.size
            canvas.create_rectangle(self.position.x - size//2, self.position.y - size,
                                    self.position.x + size//2, self.position.y + size*14/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size//4, self.position.y - size*10/4,
                                    self.position.x + size//4, self.position.y + size*3/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size//2, self.position.y - size*2,
                                    self.position.x + size//2, self.position.y + size*3/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size*3/4, self.position.y - size * 6/4,
                                    self.position.x + size*3/4, self.position.y + size * 3/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size, self.position.y - size * 3/4,
                                    self.position.x + size, self.position.y + size, fill=self.col)
        elif self.isAlive and self.grow:
            if self.startSize <= self.size:
                self.startSize += random.uniform(0.6, 1)
            else:
                self.grow = False
            size = self.startSize
            canvas.create_rectangle(self.position.x - size//2, self.position.y - size,
                                    self.position.x + size//2, self.position.y + size*14/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size//4, self.position.y - size*10/4,
                                    self.position.x + size//4, self.position.y + size*3/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size//2, self.position.y - size*2,
                                    self.position.x + size//2, self.position.y + size*3/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size*3/4, self.position.y - size * 6/4,
                                    self.position.x + size*3/4, self.position.y + size * 3/4, fill=self.col)
            
            canvas.create_rectangle(self.position.x - size, self.position.y - size * 3/4,
                                    self.position.x + size, self.position.y + size, fill=self.col)
            
        if self.makeSmaller:
            if self.size <= 0:
                self.isAlive = False
                return
            self.size -= random.uniform(1, 1.5)
            for i in self.fireImage:
                canvas.create_image(self.position.x, self.position.y, image=i)
                if random.uniform(0, 1) < 0.3:
                    canvas.create_image(self.position.x-5, self.position.y, image=i)
                    canvas.create_image(self.position.x+5, self.position.y, image=i)
                if random.uniform(0, 1) < 0.2:
                    canvas.create_image(self.position.x, self.position.y+2, image=i)
                    canvas.create_image(self.position.x-2, self.position.y+2, image=i)
                    canvas.create_image(self.position.x+2, self.position.y+2, image=i)
            
            
    
    def makeSmall(self, canvas):
        print('here')
        while self.isAlive:
            if self.size <= 0:
                self.isAlive = False
                return
            self.size -= random.uniform(0.7, 1)
            for i in self.fireImage:
                canvas.create_image(self.position.x, self.position.y, image=i)



class Animal(Organisms):
    def __init__(self, isAlive, alleles, position):
        self.isAlive = isAlive
        self.alleles = alleles
        self.position = position
        self.possibleCols = ['firebrick1', 'firebrick2', 'firebrick3', 'red', 'red2', 'red3', 'red4']
        self.col = self.getRandomColor()

    def show(self, canvas):
        canvas.create_rectangle(self.position.x - 8, self.position.y - 2,
                                self.position.x + 8, self.position.y + 2, fill=self.col)



    def getRandomColor(self):
        return random.choice(self.possibleCols)



