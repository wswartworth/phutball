
# In charge of GUI

from Action import Action
from ActionTypes import ActionTypes
from BoardStates import BoardStates
import tkinter as tk
import GameState


class Board(tk.Frame):

    cursorRow = -1
    cursorCol = -1
    cursorStoneId = -1

    # the last stone to be placed
    last = None

    def __init__(self, parent, gameState):

        tk.Frame.__init__(self, parent)
        self.gameState = gameState
        self.rows = self.gameState.rows  # number of horizontal lines
        self.cols = self.gameState.cols  # number of vertical lines
        self.hborder = 50  # left-right border
        self.vborder = 50  # top-bottom border
        self.squareSize = 40
        self.stonerad = 0.3 * self.squareSize
        w = (self.cols - 1) * self.squareSize + 2 * self.hborder
        h = (self.rows - 1) * self.squareSize + 2 * self.vborder

        # Maintain references to pieces on the board to remove as necessary
        self.boardObjects = list()

        self.board = tk.Canvas(parent, width=w, height=h)
        self.board.pack()

        # self.clickable = False #can the player click on the screen?

        for i in range(0, self.cols):
            x = self.hborder + i * self.squareSize
            self.board.create_line(x, self.vborder, x, self.vborder + self.squareSize * (self.rows - 1))

        for i in range(0, self.rows):
            y = self.vborder + i * self.squareSize
            self.board.create_line(self.hborder, y, self.hborder + self.squareSize * (self.cols - 1), y)

        self.board.bind("<Button-1>", self.onClick)
        self.board.bind("<Motion>", self.onMove)

        # self.nextTurn() #start the game

    def clearBoard(self):
        for obj in self.boardObjects():
            self.board.delete(obj)

    def clearPosition(self, position):
        self.board.delete(self.boardObjects[position])
        self.boardObjects.remove(position)

    # get nearest grid point (in L_1 norm) to given coordinates
    def row_col(self, x, y):

        r = (y - self.vborder + 0.5 * self.squareSize) // self.squareSize
        c = (x - self.hborder + 0.5 * self.squareSize) // self.squareSize
        return (r, c)

    # use the game state to update the board GUI
    def updateBoard(self):

        boardDelta: dict() = self.gameState.getBoardDelta()
        for position in boardDelta.keys():
            if (boardDelta[position] == BoardStates.Empty):
                self.clearPosition(position)
            elif (boardDelta[position] == BoardStates.Stone):
                self.drawStone(position)
            elif (boardDelta[position] == BoardStates.Ball):
                self.drawStone(position, True)
            else:
                assert False, "Found invalid BoardState when updating board"

    #called on a click
    def onClick(self,event):

        # if not self.clickable: return
        while (True):
            r, c = self.row_col(event.x, event.y)
            if (self.gameState.getStateAtPosition((r, c)) != BoardStates.Stone):
                break

        action = None
        if (self.gameState.getStateAtPosition((r, c)) == BoardStates.Empty):
            action = Action(ActionTypes.SetStone, [(r, c)])
        else:
            # The Ball was clicked. Now we need to select a sequence of stones until we hit an empty position
            action = Action(ActionTypes.MoveBall, [(r, c)])
            while (self.gameState.getStateAtPosition((r, c)) != BoardStates.Empty):
                r, c = self.row_col(event.x, event.y)

                if (self.gameState.getStateAtPosition((r, c)) == BoardStates.Stone):
                    action.appendCoordinate((r, c))

        self.gameState.applyAction(action)
        self.updateBoard()
        
    #create stone, return ID
    def drawStone(self, coords, football=False):
        r,c = coords
        center = (self.hborder + c * self.squareSize, self.vborder + r * self.squareSize)
        color = "black" if not football else "white"
        rad = self.stonerad
        return self.board.create_oval(center[0]-rad, center[1]-rad,center[0]+rad,center[1]+rad, fill=color, width = 1, outline = "black")

    #wait for a move
    def acceptMove(self):
        pass
        #self.clickable = true

    def onMove(self, event):
        pass


top = tk.Tk()
state = GameState.GameState()
board = Board(top, state)
top.mainloop()
