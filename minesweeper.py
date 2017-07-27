from tkinter import *
from tkinter.messagebox import *
import random
from collections import deque


class Minesweeper:
    def __init__(self, game):
        # Load standard tiles
        self.noTile = [] # create an empty list then populate later on
        self.flagTile = PhotoImage(file="tiles/flagTile.gif")
        self.mineTile = PhotoImage(file="tiles/mineTile.gif")
        self.plainTile = PhotoImage(file="tiles/plainTile.gif")
        self.wrongTile = PhotoImage(file="tiles/wrongTile.gif")
        self.clickedTile = PhotoImage(file="tiles/clickedTile.gif")
        # Load numbered tiles 1-8 through loop and add to list
        for tileNum in range(1, 9):
            self.noTile.append(PhotoImage(file="tiles/t" + str(tileNum) + ".gif"))

        # create a new Frame widget, used for grouping and organising other widgets
        master = Frame(game)
        master.pack()
        # create a heading label for frame
        self.firstLabel = Label(master, text="Minesweeper v1")
        self.firstLabel.grid(row=0, column=0, columnspan=10)

        # initialise main variables
        self.totalMines = 0
        self.clicked = 0
        self.totalFlags = 0
        self.correctFlags = 0
        self.cells = dict({})
        coordY = 0
        coordX = 1
        gridSize = 100 # first variable to check for grid size
        uniformCheck = 0.1
        for key in range(0, gridSize): # no. of cells
            mineCount = 0
            if random.uniform(0.0, 1.0) < uniformCheck:
                mineCount = 1
                self.totalMines += 1
            # store cell behaviour within list to be accessed
            self.cells[key] = [Button(master, image=self.plainTile), mineCount, 0, key, [coordX, coordY], 0]
            self.cells[key][0].bind('<Button-3>', self.rightClickWrapper(key)) # Button 3 = right click
                                                                           # (because button 2 is scroll)
            self.cells[key][0].bind('<Button-1>', self.leftClickWrapper(key))  # Button 1 = left click
            coordY += 1
            # 10x10
            if coordY == 10:
                coordX += 1
                coordY = 0

        for x in self.cells:
            self.cells[x][0].grid(row=self.cells[x][4][0], column=self.cells[x][4][1])

        self.secondLabel = Label(master, text="Mines: " + str(self.totalMines))
        self.secondLabel.grid(row=11, column=0, columnspan=5)
        self.thirdLabel = Label(master, text="Flags: " + str(self.totalFlags))
        self.thirdLabel.grid(row=11, column=4, columnspan=5)

        # uses similar check from emptyClear function
        for x in self.cells:
            mineClose = 0
            if self.mineCheck(x + 1):
                mineClose = mineClose + 1
            if self.mineCheck(x - 1):
                mineClose = mineClose + 1
            if self.mineCheck(x + 9):
                mineClose = mineClose + 1
            if self.mineCheck(x - 9):
                mineClose = mineClose + 1
            if self.mineCheck(x + 10):
                mineClose = mineClose + 1
            if self.mineCheck(x - 10):
                mineClose = mineClose + 1
            if self.mineCheck(x + 11):
                mineClose = mineClose + 1
            if self.mineCheck(x - 11):
                mineClose = mineClose + 1
            self.cells[x][5] = mineClose

    def tileScan(self, x, stack):
        try:
            if self.cells[x][2] == 0:
                if self.cells[x][5] == 0:
                    self.cells[x][0].config(image=self.clickedTile)
                    stack.append(x)
                else:
                    self.cells[x][0].config(image=self.noTile[self.cells[x][5] - 1])
                self.cells[x][2] = 1
                self.clicked += 1
        except KeyError:
            pass

    def leftClick(self, buttonDt):
        if buttonDt[1] == 1:
            for key in self.cells:
                if self.cells[key][1] != 1 and self.cells[key][2] == 2:
                    self.cells[key][0].config(image=self.wrongTile)
                if self.cells[key][1] == 1 and self.cells[key][2] != 2:
                    self.cells[key][0].config(image=self.mineTile)
            self.lose()
        else:
            if buttonDt[5] == 0:
                buttonDt[0].config(image=self.clickedTile)
                self.emptyClear(buttonDt[3])
            else:
                buttonDt[0].config(image=self.noTile[buttonDt[5] - 1])
            if buttonDt[2] != 1:
                buttonDt[2] = 1
                self.clicked += 1
            if self.clicked == 100 - self.totalMines: # Could use gridSize instead of fixed int length 100
                self.win()

    def emptyClear(self, key):
        # create a double-ended queue for use of removing/adding elements from either end, very useful
        stack = deque([key])
        while len(stack) != 0:
            kCheck = stack.popleft()
            # right tile
            self.tileScan(kCheck + 1, stack)
            # left tile
            self.tileScan(kCheck - 1, stack)
            # bottom right tile
            self.tileScan(kCheck + 9, stack)
            # top right tile
            self.tileScan(kCheck - 9, stack)
            # bottom middle tile
            self.tileScan(kCheck + 10, stack)
            # top middle tile
            self.tileScan(kCheck - 10, stack)
            # bottom left tile
            self.tileScan(kCheck + 11, stack)
            # top left tile
            self.tileScan(kCheck - 11, stack)

    def leftClickWrapper(self, key):
        return lambda Button: \
            self.leftClick(self.cells[key])

    def rightClickWrapper(self, key):
        return lambda Button: \
            self.rightClick(self.cells[key])

    def mineCheck(self, x):
        try:
            if self.cells[x][1] == 1:
                return True
        except KeyError:
            pass

    def rightClick(self, buttonDt):
        if buttonDt[2] == 0:
            buttonDt[2] = 2
            buttonDt[0].config(image=self.flagTile)
            buttonDt[0].unbind('<Button-1>')
            if buttonDt[1] == 1:
                self.correctFlags += 1
            self.totalFlags += 1
            self.flagUpdate()
        elif buttonDt[2] == 2:
            buttonDt[0].config(image=self.plainTile)
            buttonDt[0].bind('<Button-1>', self.leftClickWrapper(buttonDt[3]))
            buttonDt[2] = 0
            if buttonDt[1] == 1:
                self.correctFlags -= 1
            self.totalFlags -= 1
            self.flagUpdate()

    def flagUpdate(self):
        self.thirdLabel.config(text="Flags: " + str(self.totalFlags))

    def lose(self):
        msg = 'You lost! Play again?'
        answer = askquestion('Game Over', msg)
        if answer == 'yes':
            self.reset() # yet to be added
        else:
            self.quit()

    def win(self):
        msg = "Congratulations!", "You Win!"
        self.quit()

    def quit(self):
        global root
        root.quit()


def testCommand():
    print("Test output!")


def main():
    global root
    root = Tk()
    root.title("Minesweeper")
    ms = Minesweeper(root)
    menubar = Menu(root)

    # create a pulldown menu
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Standard", command=testCommand)
    filemenu.add_command(label="Hexagon", command=testCommand)
    filemenu.add_command(label="Colour", command=testCommand)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="Game Type", menu=filemenu)
    # create pulldown menu for help
    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=testCommand)
    menubar.add_cascade(label="Help", menu=helpmenu)


    # display the menu
    root.config(menu=menubar)
    # Window application loop
    root.mainloop()




if __name__ == "__main__":
    main()