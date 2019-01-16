
from enum import Enum
import copy as copy


# Enum of possible board states
class BoardStates(Enum):

    Empty = 0
    Red = 1
    Black = 2


# empty should really be a set
class GameState():

    def __init__(self, rows=8, cols=10):

        self.rows = rows
        self.cols = cols
        self.p1Turn = True
        self.boardState = {}
        self.colHeights = cols * [0] #keeps of the number of pieces per column
        self.winner = None

        # initalize the board to be empty with a ball in the middle
        for i in range(0, rows):
            for j in range(0, cols):
                self.boardState[(i, j)] = BoardStates.Empty

    def copy(self):
        stateCopy = GameState(self.rows, self.cols)
        stateCopy.p1Turn = self.p1Turn
        stateCopy.boardState = copy.copy(self.boardState)
        stateCopy.colHeights = copy.copy(self.colHeights)
        stateCopy.winner = self.winner
        return stateCopy

    def makeMove(self, col):

        color = BoardStates.Red if self.p1Turn else BoardStates.Black  #P1 is red, P2 is black
        coords = self.placeStone(col, color)
        self.p1Turn = not self.p1Turn

    def placeStone(self, col, color):
        assert not self.colFull(col) , "attempt to play in full column"
        coords = (self.colHeights[col],col)
        self.boardState[coords] = color
        self.colHeights[col] += 1
        self.winner = self.newWinner(coords)

        return coords


    def colFull(self, col):
        assert self.colHeights[col] <= self.rows, "column overfilled"
        return self.colHeights[col] == self.rows;


    #check if there's a four-in-a-row involving a giving point.  More efficient than scanning through the entire board.
    #returns the color that makes up the four-in-a-row, or None if there isn't one.
    def checkForFour(self, coords):

        posDirs = [(0,1), (1,1), (1,0), (1,-1)]

        r,c = coords
        color = self.boardState[coords]
        #print("color: ", color)
        if color == BoardStates.Empty: return None

        for pdir in posDirs:
            pcount=0
            ncount=0

            for i in range(1,4):
                nextSpot = (r+i*pdir[0],c+i*pdir[1])
                if (self.inBounds(nextSpot) and self.boardState[nextSpot] == color):
                    pcount += 1
                else:
                    break
            for i in range(1,4):
                nextSpot = (r-i*pdir[0],c-i*pdir[1])
                if (self.inBounds(nextSpot) and self.boardState[nextSpot] == color):
                    ncount +=  1
                else:
                    break

            lineLen = ncount+pcount+1
            if(lineLen >= 4):
                return color
            else:
                return None

    def newWinner(self, coords):
        winningColor = self.checkForFour(coords)
        if winningColor == BoardStates.Red: 
            #print("new: 1")
            return 1
        if winningColor == BoardStates.Black: 
            #print("new: -1")
            return -1
        #print("new: none")
        return None

    def inBounds(self, coords):
        r, c = coords[0], coords[1]
        return (0 <= r <= self.rows-1) and (0 <= c <= self.cols-1)

    def getWinner(self):
        return self.winner

    def legalMoves(self):

        if self.winner != None: 
            return []

        moves = []
        for c in range(0,self.cols):
            if not self.colFull(c):
                moves.append(c)
        return moves



   