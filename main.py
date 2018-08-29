from tkinter import *
import math
from vector import *
import random
from Button import Button
from Star import Star
from Islands import Islands


# MODEL VIEW CONTROLLER (MVC)
####################################
# MODEL:       the data
# VIEW:        redrawAll and its helper functions
# CONTROLLER:  event-handling functions and their helper functions
####################################


####################################
# customize these functions
####################################


# Initialize the data which will be used to draw on the screen.
def init(data):
    # load data as appropriate
    data.stars = []
    data.numStars = 250
    makeStars(data)
    data.screenMode = 'splash'
    data.isPaused = False
    data.myIsland = []
    data.specieType = 'Tree'
    data.genOrganisms = False
    data.frequenciesOrganisms = []
    data.startButton = ''
    data.backButton = ''
    data.removeAllele = []
    data.button11, data.button7, data.button8, data.button9, data.button10 = False, False, False, False, False
    data.flameImages = [PhotoImage(file='flame/flame.gif',format = 'gif -index %i' %(i)) for i in range(1, 7)]
    data.helpImages = [PhotoImage(file='images/help1.gif', format='gif'), PhotoImage(file='images/help2.gif', format='gif')]

def makeIslands(data):
    data.myIsland = []
    data.myIsland.append(Islands((190, 170), 'Population 1', data.specieType, data.flameImages))
    data.myIsland[0].makePointsIslands()

    data.myIsland.append(Islands((190, data.height - 270), 'Population 2', data.specieType, data.flameImages))
    data.myIsland[1].makePointsIslands()

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

def makeStars(data):
    for i in range(data.numStars):
        startAngle = random.uniform(0, 2 * math.pi)
        currVector = Vector.fromAngle(startAngle) * 3
        data.stars.append(Star(data, currVector, rgbString(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))


def mutation(data):
    islandOne = data.myIsland[0]
    islandTwo = data.myIsland[1]
    for i in range(len(islandOne.organisms)):
        if random.uniform(0, 1) < 0.1:
            curr = islandOne.organisms[i].alleles
            newHalf = random.choice(curr)
            otherHalf = random.choice('TTttTtRB')
            newAllele = newHalf + otherHalf
            if newAllele == 'tT':
                newAllele = 'Tt'
            elif newAllele == 'Rt':
                newAllele = 'tR'
            elif newAllele == 'RT':
                newAllele = 'TR'
            elif newAllele == 'BT':
                newAllele = 'TB'
            elif newAllele == 'Bt':
                newAllele = 'tB'
            islandOne.addOneTree(newAllele)
            islandOne.organisms.pop(i)
        
    for i in range(len(islandTwo.organisms)):
        if random.uniform(0, 1) < 0.1:
            curr = islandTwo.organisms[i].alleles
            newHalf = random.choice(curr)
            otherHalf = random.choice('TTttTtRB')
            newAllele = newHalf + otherHalf
            if newAllele == 'tT':
                newAllele = 'Tt'
            elif newAllele == 'Rt':
                newAllele = 'tR'
            elif newAllele == 'RT':
                newAllele = 'TR'
            elif newAllele == 'BT':
                newAllele = 'TB'
            elif newAllele == 'Bt':
                newAllele = 'tB'
            islandTwo.addOneTree(newAllele)
#             islandOne.organisms[i].makeSmaller = True
            islandTwo.organisms.pop(i)
            

def recombination(data, island):
    if len(data.myIsland) > 2:
        data.myIsland.pop()
    islandOne = island[0]
    islandTwo = island[1]
    newIsland = Islands((550, 300), 'Population 3', data.specieType, data.flameImages)
    newAlleles = []
    for parentOne in islandOne.organisms:
        pickOne = random.choice(parentOne.alleles)
        print('Pick One', pickOne)
        pickTwo = random.choice(random.choice(islandTwo.organisms).alleles)
        print('Pick Two', pickTwo)
        newAllele = pickOne + pickTwo
        if newAllele == 'tT':
            newAllele = 'Tt'
        newIsland.addOneTree(newAllele)
    newIsland.makePointsIslands()
    data.myIsland.append(newIsland)
        


# These are the CONTROLLERs.
# IMPORTANT: CONTROLLER does *not* draw at all!
# It only modifies data according to the events.

def mousePressed(event, data):
    if data.isPaused:
        return
    x, y = event.x, event.y
    if data.screenMode == 'help':
        if data.backButton and data.backButton.inButton(x, y):
            data.screenMode = 'splash'
    if data.screenMode != 'chooseProcess':
        if data.backButton.inButton(x, y):
            data.screenMode = 'chooseProcess'
            data.myIsland = []
            makeIslands(data)
            makeOrganisms(data)
            
    if data.screenMode == 'geneticDrift':
        if data.startButton.inButton(x, y):
            geneticDrift(data.myIsland[0], data)
            geneticDrift(data.myIsland[1], data)
    if data.screenMode == 'recombination':
        if data.startButton.inButton(x, y):
            # Do recombination
            recombination(data, data.myIsland)
    if data.screenMode == 'migration':
        if data.startButton.inButton(x, y):
            # Do migration
            numToChange = random.randint(0, 40)
            myAllele = random.choice([('Tt'), ("TT"), ('tt')])
            index = random.choice([0, 1])
            if index == 0:
                index1 = 1
            else:
                index1 = 0
            migration(data.myIsland[index], myAllele, 'r', numToChange, data)
            migration(data.myIsland[index1], myAllele, 'a', numToChange, data)
    if data.screenMode == 'mutation':
        if data.startButton.inButton(x, y):
            mutation(data)
    if data.screenMode == 'chooseProcess':
        if data.button7 and data.button7.inButton(x, y):
            data.screenMode = 'geneticDrift'
        if data.button8 and data.button8.inButton(x, y):
            data.screenMode = 'recombination'
        if data.button9 and data.button9.inButton(x, y):
            data.screenMode = 'mutation'
        if data.button10 and data.button10.inButton(x, y):
            data.screenMode = 'migration'
        if data.button11 and data.button11.inButton(x, y):
            data.screenMode = 'naturalSelection'

    if data.screenMode == 'splash':
        if data.button1 and data.button1.inButton(x, y):
            print('button1')
            # data.screenMode = 'chooseAnimal'
            data.screenMode = 'chooseProcess'
        if data.button2 and data.button2.inButton(x, y):
            print('button2')
            data.screenMode = 'help'
        if data.button3 and data.button3.inButton(x, y):
            print('button3')
            data.screenMode = 'about'
    if data.screenMode == 'chooseAnimal':
        if data.button5 and data.button5.inButton(x, y):
            data.specieType = 'Tree'
            data.screenMode = 'game'
            makeIslands(data)
        if data.buttondata.button6.inButton(x, y):
            data.specieType = 'Animal'
            data.screenMode = 'game'
            makeIslands(data)
    if data.screenMode == "help":
        if data.button1 and data.button1.inButton(x, y):
            data.screenMode = "splash"

def geneticDrift(island, data):
    alleles = [('Tt'), ("TT"), ('tt')]
    mypick = random.choice(alleles)
    for organism in island.organisms:
        if random.uniform(0, 1) < 0.6 and organism.alleles == mypick:
            organism.makeSmaller = True
            removeAllele = [i for i in alleles if i != mypick]
            print('mypick', mypick)
            print('remove', removeAllele)
            island.addOneTree(removeAllele)
            island.checkOrganisms(removeAllele)

def migration(island, myallele, action, numToRemove, data):
    if action == 'r':
        count = 0
        while count < numToRemove:
            num = random.randint(0, len(island.organisms)-1)
            island.organisms.pop(num)
            count += 1
    elif action == 'a':
        count = 0
        print("myallele", myallele)
        while count < numToRemove:
            island.addOneTree(myallele)
            count += 1


def makeOrganisms(data):
    for island in data.myIsland:
        island.addOrganisms()

def keyPressed(event, data):
    # use event.char and event.keysym
    key = event.keysym
    pass


def timerFired(data):
    pass


def showSplashScreen(canvas, data):
    canvas.create_text(data.width//2, data.height//5 - 80, text='EvoSim', font = ('Helvetica', '50'))
    data.button1 = Button(Vector(data.width // 2, data.height // 5),
                          canvas, data, 'Start', 100, 100)
    data.button1.showButton()

    data.button2 = Button(Vector(data.width // 2, data.height // 5 + 140),
                          canvas, data, 'Help', 100, 100)
    data.button2.showButton()

    data.button3 = Button(Vector(data.width // 2, data.height // 5 + 280),
                          canvas, data, 'About', 100, 100)
    data.button3.showButton()


def showStars(canvas, data):
    for star in data.stars:
        star.draw(canvas)
        star.move()
    for star in data.stars:
        star.offScreen()


def showHelp(canvas, data):
    # Show help
    canvas.create_image(303, 370, image=data.helpImages[0])
    canvas.create_image(904, 363, image=data.helpImages[1])
    data.button1 = Button(Vector(data.width - 80, data.height // 5 + 250),
                          canvas, data, 'Back', 80, 80)
    data.button1.showButton()



# This is the VIEW
# IMPORTANT: VIEW does *not* modify data at all!
# It only draws on the canvas.
def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill = 'pale turquoise')
    data.startButton = Button(Vector(data.width - 380, data.height // 5 + 430),
                          canvas, data, 'Start', 70, 90)
    data.backButton = Button(Vector(data.width - 150, data.height//5 + 430), canvas, data, 'Back', 70, 90)
    if data.screenMode == 'chooseAnimal':
        showChooseAnimal(canvas, data)
    elif data.screenMode == 'chooseProcess':
        data.backButton.showButton()
        canvas.create_text(data.width//2, 100, text='Factors affecting Hardy-Weinberg equilibrium', font=('Helvetiva', '45', 'bold'))
        if not data.genOrganisms:
            makeIslands(data)
            makeOrganisms(data)
            data.genOrganisms = True

        showGameButtons(canvas, data)
    elif data.screenMode == 'geneticDrift':
        # Show the program
        for island in data.myIsland:
            island.showIsland(canvas)
            island.showOrganisms(canvas)
        
        showNumOrganisms(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                         data.width - 580, 50, data.myIsland[0].title)
        showNumOrganisms(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                         data.width - 580, 230, data.myIsland[1].title)
        showFrequencies(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                        data.width - 250, 50, data.myIsland[0].title, data.myIsland[0].organisms)

        showFrequencies(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                        data.width - 250, 230, data.myIsland[1].title, data.myIsland[1].organisms)
        data.startButton.showButton()
        data.backButton.showButton()
    elif data.screenMode == 'naturalSelection':
        # Show the program
        for island in data.myIsland:
            island.showIsland(canvas)
            island.showOrganisms(canvas)
        
        showNumOrganisms(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                         data.width - 280, 50, data.myIsland[0].title)
        showNumOrganisms(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                         data.width - 280, 230, data.myIsland[1].title)
        showFrequencies(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                        data.width - 50, 50, data.myIsland[0].title, data.myIsland[0].organisms)

        showFrequencies(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                        data.width - 50, 230, data.myIsland[1].title, data.myIsland[1].organisms)
        data.startButton.showButton()
        data.backButton.showButton()
    elif data.screenMode == 'recombination':
        # Show the program
        for island in data.myIsland:
            island.showIsland(canvas)
            island.showOrganisms(canvas)
        
        showNumOrganisms(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                         data.width - 300, 50, data.myIsland[0].title)
        showNumOrganisms(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                         data.width - 300, 230, data.myIsland[1].title)
        showFrequencies(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                        data.width - 70, 50, data.myIsland[0].title, data.myIsland[0].organisms)

        showFrequencies(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                        data.width - 70, 230, data.myIsland[1].title, data.myIsland[1].organisms)
        
        if len(data.myIsland) > 2 and data.myIsland[2]:
            showFrequencies(canvas, data, data.myIsland[2].getFrequencies(data.myIsland[2].organisms),
                        data.width - 70, 430, data.myIsland[2].title, data.myIsland[2].organisms)
            
            showNumOrganisms(canvas, data, data.myIsland[2].getFrequencies(data.myIsland[2].organisms),
                         data.width - 300, 430, data.myIsland[2].title)
        data.startButton.showButton()
        data.backButton.showButton()
    elif data.screenMode == 'migration':
        # Show the program
        for island in data.myIsland:
            island.showIsland(canvas)
            island.showOrganisms(canvas)
        
        showNumOrganisms(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                         data.width - 580, 50, data.myIsland[0].title)
        showNumOrganisms(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                         data.width - 580, 230, data.myIsland[1].title)
        showFrequencies(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                        data.width - 250, 50, data.myIsland[0].title, data.myIsland[0].organisms)

        showFrequencies(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                        data.width - 250, 230, data.myIsland[1].title, data.myIsland[1].organisms)
        data.startButton.showButton()
        data.backButton.showButton()
    elif data.screenMode == 'mutation':
        # Show the program
        for island in data.myIsland:
            island.showIsland(canvas)
            island.showOrganisms(canvas)
        
        showNumOrganisms(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                         data.width - 100, 50, data.myIsland[0].title)
        showNumOrganisms(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                         data.width -280, 50, data.myIsland[1].title)
        
        showFrequencies(canvas, data, data.myIsland[0].getFrequencies(data.myIsland[0].organisms),
                        data.width - 480, 50, data.myIsland[0].title, data.myIsland[0].organisms)

        showFrequencies(canvas, data, data.myIsland[1].getFrequencies(data.myIsland[1].organisms),
                        data.width - 480, 350, data.myIsland[1].title, data.myIsland[1].organisms)
        data.startButton.showButton()
        data.backButton.showButton()
    elif data.screenMode == 'game':
        pass
    elif data.screenMode == 'splash':
        # print("Splash screen...")
        showStars(canvas, data)
        showSplashScreen(canvas, data)
    elif data.screenMode == 'help':
        showHelp(canvas ,data)
    elif data.screenMode == 'about':
        print("about screen...")
        showAboutScreen(canvas, data)

def showGameButtons(canvas, data):
    # Show buttons for the main game screen
    # buttons 7, 8, 9,10  and 11
    data.button7 = Button(Vector(data.width//2, data.height - 600), canvas, data, "Genetic Drift", 300, 40, 20)
    data.button8 = Button(Vector(data.width//2, data.height - 500), canvas, data, "Recombination", 300, 40, 20)
    data.button9 = Button(Vector(data.width//2, data.height - 400), canvas, data, "Mutation", 300, 40, 20)
    data.button10 = Button(Vector(data.width//2, data.height - 300), canvas, data, "Migration", 300, 40, 18)
#     data.button11 = Button(Vector(data.width//2, data.height - 300), canvas, data, "Natural Selection", 55, 40, 13)

    data.button7.showButton()
    data.button8.showButton()
    data.button9.showButton()
    data.button10.showButton()
#     data.button11.showButton()

def showChooseAnimal(canvas, data):
    data.button5 = Button(Vector(data.width // 2, data.height // 5),
                          canvas, data, 'Plants', 100, 100)
    data.button5.showButton()

    data.button6 = Button(Vector(data.width // 2, data.height // 5 + 140),
                          canvas, data, 'Animals', 100, 100)
    data.button6.showButton()

def showAboutScreen(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height, fill='white')
    canvas.create_text(data.width // 2, data.height // 2 - 50,
                            font=('Helvetica', '45', 'bold'),
                       text="Coded with Love and Coffee ;) ", fill='black', anchor='s')
    canvas.create_text(data.width // 2, data.height // 2 + 60,
                    font=('Helvetica', '45', 'bold'),
                       text="From : Samyak ", fill='black')

    canvas.create_text(data.width // 2, data.height // 2 + 70,
                       font=('Helvetica', '45', 'bold'),
                       text="", fill='black')
    showStars(canvas, data)

def showNumOrganisms(canvas, data, frequencies, startX, startY, popName):
    canvas.create_text(startX, startY - 40, text=popName + ' genotypes ', font=('Helvetica', '18'))
    for name in frequencies:
        if data.specieType == 'Tree':
            canvas.create_rectangle(startX - 2, startY - 4,
                                    startX + 2, startY + 14, fill=frequencies[name][1])
            canvas.create_rectangle(startX - 1, startY - 10,
                                    startX + 1, startY + 3, fill=frequencies[name][1])
            canvas.create_rectangle(startX - 2, startY - 8,
                                    startX + 2, startY + 3, fill=frequencies[name][1])
            canvas.create_rectangle(startX - 3, startY - 6,
                                    startX + 3, startY + 3, fill=frequencies[name][1])
            canvas.create_rectangle(startX - 4, startY - 3,
                                    startX + 4, startY + 4, fill=frequencies[name][1])
        canvas.create_text(startX + 50, startY, text="  " + str(frequencies[name][0]), font=('Helvetica', '18'))
        if frequencies[name][0] <= 0:
            for island in data.myIsland:
                if island.title == popName:
                    island.extinct.add(name)
#                     print('added', name)
#                 else:
#                     print("no extinct")
        canvas.create_text(startX + 80, startY, text="  " + str(name))

        startY += 50

def showFrequencies(canvas, data, frequencies, startX, startY, popName, organismsIsland):
    canvas.create_text(startX - 20, startY - 40, text=popName + ' frequencies', font=('Helvetica', '16'))
    numTInPop = 0
    numtInPop = 0
    numBinPop = 0
    numRinPop = 0
    totalPop = len(organismsIsland)*2
    for name in frequencies:
        if name == "TT":
            numTInPop += 2 * frequencies[name][0]
        elif name == 'Tt':
            numTInPop += 1 * frequencies[name][0]
            numtInPop += 1 * frequencies[name][0]
        elif name == 'tt':
            numtInPop += 2 * frequencies[name][0]
        elif name == 'TB':
            numBinPop += 1 * frequencies[name][0]
            numTInPop += 1 * frequencies[name][0]
        elif name == 'TR':
            numRinPop += 1 * frequencies[name][0]
            numTInPop += 1 * frequencies[name][0]
        elif name == 'tB':
            numBinPop += 1 * frequencies[name][0]
            numtInPop += 1 * frequencies[name][0]
        elif name == 'tR':
            numRinPop += 1 * frequencies[name][0]
            numtInPop += 1 * frequencies[name][0]
    freqT = numTInPop/totalPop * 100 if numTInPop != 0 else 0
    freqt = numtInPop/totalPop * 100 if numtInPop != 0 else 0
    freqB = numBinPop/totalPop * 100 if numBinPop != 0 else 0
    freqR = numRinPop/totalPop * 100 if numRinPop != 0 else 0
    canvas.create_text(startX, startY, text="Freq T", font=('Helvetica', '16'))
    canvas.create_rectangle(startX - 30, startY - 25, startX + 30, startY + 25)
    canvas.create_text(startX - 60, startY, text="%0.1f"%(freqT), font=('Helvetica', '18'), fill='red')
    canvas.create_rectangle(startX - 90, startY - 25, startX - 30, startY + 25)
    canvas.create_text(startX, startY + 50, text="Freq t", font=('Helvetica', '16'))
    canvas.create_rectangle(startX - 30, startY + 25, startX + 30, startY + 75)
    canvas.create_text(startX - 60, startY + 50, text="%0.1f"%(freqt), font=('Helvetica', '18'), fill='red')
    canvas.create_rectangle(startX - 90, startY + 25, startX + 30, startY + 75)
    if numBinPop != 0:
        canvas.create_text(startX, startY + 100, text="Freq B", font=('Helvetica', '16'))
        canvas.create_rectangle(startX - 30, startY + 75, startX + 30, startY + 125)
        canvas.create_text(startX - 60, startY + 100, text="%0.1f"%(freqB), font=('Helvetica', '18'), fill='red')
        canvas.create_rectangle(startX - 90, startY + 75, startX - 30, startY + 125)
    if numRinPop != 0:
        canvas.create_text(startX, startY +150, text="Freq R", font=('Helvetica', '16'))
        canvas.create_rectangle(startX - 30, startY + 125, startX + 30, startY + 175)
        canvas.create_text(startX - 60, startY +150, text="%0.1f"%(freqR), font=('Helvetica', '18'), fill='red')
        canvas.create_rectangle(startX - 90, startY + 125, startX - 30, startY + 175)


# The beautiful run function in main taken from : https://pd43.github.io/notes/notes4-2.html
####################################
####################################
# use the run function as-is
####################################
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()
    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        # redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object):
        pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 10  # millisecond
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    init(data)
    data.canvas = canvas
    # set up events
    root.bind("<Button-1>", lambda event:
              mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
              keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")


run(1200, 800)
