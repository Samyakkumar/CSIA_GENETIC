class Button(object):
    def __init__(self, location, canvas, data, message, xsize, ysize, fontSize=24):
        self.location = location # Location passed as a vector
        self.canvas = canvas # The canvas on which the button should be drawn
        self.data = data # Global data variable
        self.message = message # The text for the button
        self.xsize = xsize # Width
        self.ysize = ysize  # Height
        self.fontSize = fontSize
        self.fill = 'white' # Background fill for the button


    def showButton(self): # Display the button on the screen
        self.canvas.create_rectangle(self.location.x - self.xsize, self.location.y,
                                     self.location.x + self.xsize,
                                     self.location.y + self.ysize, outline='black', fill = self.fill)
        self.canvas.create_text(self.location.x,
                                self.location.y + self.ysize//3,
                                font=('Helvetica', str(self.fontSize)),
                                text=self.message, fill='black', anchor='n')

    def inButton(self, x, y): # Check if a click is inside the button
        check = (x > self.location.x - self.xsize and x < self.location.x + self.xsize
                 and y > self.location.y and y < self.location.y + self.ysize)
        if check:
            self.fill = 'black'
        return check
