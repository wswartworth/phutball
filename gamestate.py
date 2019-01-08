
#empty should really be a set
class GameState():
    
    EMPTY = 0
    STONE = 1
    BALL = 2
  
    def __init__(self, rows=19, cols=15):

        self.rows = rows
        self.cols = cols
        self.p1Turn = True

        self.ball = (self.rows//2, self.cols//2)

        self.boardState = {}
        #initalize the board to be empty with a ball in the middle
        for i in range(0,rows):
            for j in range(0,cols):
                boardState[(i,j)] = EMPTY
        boardState[ball] = BALL
    
    def setStone(self, coords):
        assert (boardState[coords] == EMPTY):
        self.boardState[coords] = STONE

    def inBounds(self,coords):
        r,c = coords[0], coords[1]
        return (r>=0 and r<=self.rows-1 and c>=0 and c<=self.cols-1)
                

  
  