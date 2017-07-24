from tkinter import *
from tkinter.messagebox import *
import random
from collections import deque


class Minesweeper:
    def __init__(self, game):
        # Load standard tiles
        self.noTile = []
        self.flagTile = PhotoImage(file="tiles/flagTile.gif")
        self.mineTile = PhotoImage(file="tiles/mineTile.gif")
        self.plainTile = PhotoImage(file="tiles/plainTile.gif")
        self.wrongTile = PhotoImage(file="tiles/wrongTile.gif")
        self.clickedTile = PhotoImage(file="tiles/clickedTile.gif")
        # Load numbered tiles 1-8 through loop
        for tileNum in range(1, 9):
            self.noTile.append(PhotoImage(file="tiles/t" + str(tileNum) + ".gif"))

        master = Frame(game)
        master.pack()
        self.firstLabel = Label(master, text="Minesweeper v1")
        self.firstLabel.grid(row=0, column=0, columnspan=10)

        self.totalMines = 0
        self.clicked = 0
        self.totalFlags = 0
        self.correctFlags = 0
        self.cells = dict({})
        coordY = 0
        coordX = 1

        for x in range(0, 100): # no. of cells
            mineCount = 0
            setGraphics = self.plainTile
            if random.uniform(0.0, 1.0) < 0.1:
                mineCount = 1
                self.totalMines += 1
            self.cells[x] = [Button(master, image=setGraphics), mineCount, 0, x, [coordX, coordY], 0]

            coordY += 1
            if coordY == 10:
                coordX += 1
                coordY = 0

        for x in self.cells:
            self.cells[x][0].grid(row=self.cells[x][4][0], column=self.cells[x][4][1])

        self.secondLabel = Label(master, text="Mines: " + str(self.totalMines))
        self.secondLabel.grid(row=11, column=0, columnspan=5)

        self.thirdLabel = Label(master, text="Flags: " + str(self.totalFlags))
        self.thirdLabel.grid(row=11, column=4, columnspan=5)

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

    def leftClickWrapper(self, key):
        return lambda Button: \
            self.leftClick(self.cells[key])

    def rightClickWrapper(self, key):
        return lambda Button: \
            self.rightClick(self.cells[key])

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
        msg = "Game Over", "You Lose!"
        global root
        root.destroy()

    def win(self):
        msg = "Congratulations!", "You Win!"
        global root
        root.destroy()



def main():
    global root
    root = Tk()
    root.title("Minesweeper")
    ms = Minesweeper(root)
    root.mainloop()


if __name__ == "__main__":
    main()