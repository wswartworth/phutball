
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

        # board settings
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
        self.boardObjects = dict()

        self.board = tk.Canvas(parent, width=w, height=h)
        self.board.pack()

        # Initialize board
        for i in range(0, self.cols):
            x = self.hborder + i * self.squareSize
            self.board.create_line(x, self.vborder, x, self.vborder + self.squareSize * (self.rows - 1))

        for i in range(0, self.rows):
            y = self.vborder + i * self.squareSize
            self.board.create_line(self.hborder, y, self.hborder + self.squareSize * (self.cols - 1), y)

        self.drawStone(self.gameState.getBallPosition(), football=True)

        self.board.bind("<Button-1>", self.onClick)
        self.board.bind("<Motion>", self.onMove)

        # For gameplay
        self.playerOneTurn = True
        self.executingBallMoveAction = False
        self.ballMovePositions = list()

    def clearBoard(self):

        for coordinate in self.boardObjects.keys():
            self.clearPosition(coordinate)

    def clearPosition(self, position):

        self.board.delete(self.boardObjects[position])
        self.boardObjects[position] = None

    def distance(self, position1, position2):

        return abs(position1[0] - position2[0]) + abs(position1[1] - position2[1])

    def drawStone(self, coords, football=False):
        
        r, c = coords
        center = (self.hborder + c * self.squareSize, self.vborder + r * self.squareSize)
        color = "black" if not football else "white"
        rad = self.stonerad
        boardObject = self.board.create_oval(
            center[0]-rad,
            center[1]-rad,
            center[0]+rad,
            center[1]+rad,
            fill=color,
            width=1,
            outline="black")

        self.boardObjects[coords] = boardObject

    def executingBallMove(self, position, positionState):

        if (positionState is BoardStates.Ball):
            return

        assert self.distance(self.ballMovePositions[-1], position) <= 2, "Stones must be adjacent during ball move."
        self.ballMovePositions.append(position)

        if (positionState is BoardStates.Empty):
            action = Action(ActionTypes.MoveBall, self.ballMovePositions)
            self.gameState.applyAction(action)
            self.updateBoard()
            self.ballMovePositions = list()
            self.executingBallMoveAction = False

    def onClick(self, event):

        r, c = self.row_col(event.x, event.y)
        positionState = self.gameState.getStateAtPosition((r, c))

        if (self.executingBallMoveAction):
            self.executingBallMove((r, c), positionState)
            return

        if (positionState is BoardStates.Empty):
            # We just want to place a stone there
            action = Action(ActionTypes.SetStone, [(r, c)])
            self.gameState.applyAction(action)
            self.updateBoard()

        if (positionState is BoardStates.Ball):
            # Initiate MoveBall action
            self.ballMovePositions.append((r, c))
            self.executingBallMoveAction = True

    def onMove(self, event):
        pass

    # get nearest grid point (in L_1 norm) to given coordinates
    def row_col(self, x, y):

        r = (y - self.vborder + 0.5 * self.squareSize) // self.squareSize
        c = (x - self.hborder + 0.5 * self.squareSize) // self.squareSize

        assert self.gameState.inBounds((r, c)), "Selected point is not on the board."
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


top = tk.Tk()
state = GameState.GameState()
board = Board(top, state)
top.mainloop()
