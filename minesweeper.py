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