from Tkinter import *
from Dice import diceArray4x4, diceArray5x5
from random import randint

class App():
    color = 'white'
    gridColor = "#648EBD"

    leftMargin = 20

    newGameButtonX = leftMargin
    newGameButtonY = 20

    clockX = leftMargin
    clockY = newGameButtonY + 60

    radio1X = leftMargin
    radio1Y = clockY + 100

    radio2X = leftMargin
    radio2Y = radio1Y + 40

    gridCount = 5
    gridX = clockX + 150
    gridY = clockY
    gridSize = 100 * gridCount
    gridSpacing = 100
    gridThickness = 3

    letterPaddingX = 20
    letterPaddingY = 12

    curSize = 5


    letterLabelDict = {}

    countingJob = None

    letterArray = []






    def __init__(self):
        self.root = Tk()
        self.root.title("Super Boggle")
        self.setupFrontend()




    def setupFrontend(self):


        #setup grid
        self.theGrid = Canvas(self.root, width=self.gridSize, height=self.gridSize)
        self.theGrid.place(x = self.gridX, y = self.gridY)
        self.setupGrid()



        self.setupLetters()


        #setup timer
        self.timerLabel = Label(text="3:00", font=("Avenir Next", 36))
        self.timerLabel.place(x=self.clockX, y=self.clockY)

        #setup Button
        startButton = Button(self.root, text="New Game", highlightbackground=self.color, command=self.newGame)
        startButton.place(x=self.newGameButtonX, y=self.newGameButtonY)


        self.gridVar = IntVar()

        radioButton1 = Radiobutton(self.root, text="4x4", variable=self.gridVar, command=self.setGridSize, value=4, font=("Avenir Next", 20))
        radioButton1.place(x=self.radio1X, y=self.radio1Y)
        radioButton2 = Radiobutton(self.root, text="5x5", variable=self.gridVar, value=5, font=("Avenir Next", 20))
        radioButton2.invoke()
        radioButton2.config(command=self.setGridSize)
        radioButton2.place(x=self.radio2X, y=self.radio2Y)


        #setup window
        self.root.config(bg=self.color, width=self.gridX + self.gridSize + 100, height=self.gridY + self.gridSize + 100)


        self.root.mainloop()


    #Gets letters, resets the clock, displays the letters
    def newGame(self):
        if self.countingJob:
            self.root.after_cancel(self.countingJob)

        self.remainingTime = 180
        self.timerLabel.config(fg="black")
        self.letterArray = self.getRandomizedLetters()
        self.setBoard()
        self.update_clock()

    #recursively calls itself to countdown from 3 minutes
    def update_clock(self):

        minutes = str(self.remainingTime/60)
        seconds = self.remainingTime%60
        if seconds < 10:
            seconds = "0" + str(seconds)
        else:
            seconds = str(seconds)
        timeString = (minutes + ":" + seconds)
        self.remainingTime -= 1
        self.timerLabel.configure(text=timeString)
        if self.remainingTime >= 0:
            self.countingJob = self.root.after(1000, self.update_clock)
        else:
            self.timerLabel.config(fg="red")

    #resets the letters when the button is pressed
    def setBoard(self):
        if len(self.letterArray) == 0:
            return

        i = 0
        for key in self.letterLabelDict:
            if self.gridCount == 4:
                if int(key[-1]) % 5 == 4:
                    self.letterLabelDict[key].config(text = "")
                    continue
                if i > 15:
                    self.letterLabelDict[key].config(text = "")
                    continue

            if self.letterArray[i] == "q" or self.letterArray[i] == "Q":
                newLetter = "Qu"
            else:
                newLetter = self.letterArray[i].upper()
            self.letterLabelDict[key].config(text = newLetter)
            i += 1


    #selects new random letters from the dice
    def getRandomizedLetters(self):

        diceRange = range(0,self.gridCount*self.gridCount)
        print(self.gridCount)
        gameLetters=[]

        #this loop randomly selects a cube and a letter from that cube without replacement for cubes
        #It then puts the letter in gameLetters
        while(len(diceRange)):
            randomIndex = diceRange[randint(0,len(diceRange)-1)]
            if self.gridCount == 4:
                randomlySelectedCube = diceArray4x4[randomIndex]
            else:
                randomlySelectedCube = diceArray5x5[randomIndex]
            gameLetters.append(randomlySelectedCube[randint(0,5)])
            diceRange.remove(randomIndex)

        return gameLetters

    def setGridSize(self):
        self.gridCount = self.gridVar.get()
        self.gridSize = self.gridSpacing*self.gridCount
        if self.gridCount == self.curSize:
            return


        self.curSize = self.gridCount
        self.setupGrid()
        self.newGame()


    def setupLetters(self):
        for i in range(0,25):
            newLetter = Label(text="X", font=("Avenir Next", 56), width=2)
            newLetter.place(x=self.gridX + i%self.gridCount*self.gridSpacing + self.letterPaddingX, y=self.gridY + i/self.gridCount*self.gridSpacing + self.letterPaddingY)
            self.letterLabelDict["letter{0}".format(i)]=newLetter

    def setupGrid(self):

        self.theGrid.config(width=self.gridSize, height=self.gridSize)
        i = 1
        self.theGrid.delete("all")
        while i < self.gridCount:
            startPoint = i * self.gridSpacing
            self.theGrid.create_rectangle(0, startPoint, self.gridSize, startPoint + self.gridThickness, fill=self.gridColor, outline=self.gridColor)
            self.theGrid.create_rectangle(startPoint, 0, startPoint + self.gridThickness, self.gridSize, fill=self.gridColor, outline=self.gridColor)
            i +=1



app = App()



