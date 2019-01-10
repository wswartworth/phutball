
import copy

EMPTY = 0
STONE = 1
BALL = 2

#empty should really be a set
class GameState():
  
    def __init__(self, rows=21, cols=15):

        self.rows = rows
        self.cols = cols
        self.p1Turn = True

        self.ball = (self.rows//2, self.cols//2)

        self.boardState = {}
        #initalize the board to be empty with a ball in the middle
        for i in range(0,rows):
            for j in range(0,cols):
                self.boardState[(i,j)] = EMPTY
        self.boardState[self.ball] = BALL

    def copy(self):
        selfCopy = GameState(self.rows, self.cols)
        selfCopy.ball = self.ball
        selfCopy.p1Turn = self.p1Turn
        selfCopy.boardState = copy.copy(self.boardState)
        return selfCopy

    def setStone(self, coords):
        assert (self.boardState[coords] == EMPTY)
        self.boardState[coords] = STONE

    #all the squares the ball can jump to
    def legalJumpSquares(self):
        dirs = [(0,1), (1,0), (1,1), (0,-1), (-1,0), (-1,1), (1,-1), (-1,-1)]
        legalJumps = []
        for d in dirs:
            curSquare = self.ball
            jumpLen = 0
            while True:
                curSquare = (curSquare[0] + d[0], curSquare[1] + d[1])
                if not curSquare in self.boardState: break
                if self.boardState[curSquare] != STONE: break
                jumpLen += 1
            if self.inBounds(curSquare) and jumpLen > 0:
                legalJumps.append(curSquare)
        return legalJumps


    def jumpInDir(self, d):
        curSquare = self.ball
        while True:
            curSquare = (curSquare[0] + d[0], curSquare[1] + d[1])
            if self.boardState[curSquare] == EMPTY: 
                break
            elif self.boardState[curSquare] == STONE:
                self.boardState[curSquare] = EMPTY
            else: 
                assert(True)
        self.boardState[self.ball] = EMPTY
        self.ball = curSquare
        self.boardState[curSquare] = BALL

    #assumes the jump square is legal
    def jumpTo(self, coords):
        def sgn(n):
            if n == 0: return 0
            if n < 0: return -1
            if n > 0: return 1
        bearing = (sgn(coords[0] - self.ball[0]), sgn(coords[1] - self.ball[1]))
        self.jumpInDir(bearing)
        print(self.boardState)






    def inBounds(self,coords):
        r,c = coords[0], coords[1]
        return (r>=0 and r<=self.rows-1 and c>=0 and c<=self.cols-1)
                

  
  