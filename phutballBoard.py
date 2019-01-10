import tkinter as tk
import gamestate
import copy

class Board(tk.Frame):

    cursorRow=-1
    cursorCol=-1
    cursorStoneId = -1
    last = None #the last stone to be placed

    #get nearest grid point (in L_1 norm) to given coordinates
    def row_col(self,x,y):
        r = (y-self.vborder + 0.5*self.squaresize)//self.squaresize
        c = (x-self.hborder+ 0.5*self.squaresize)//self.squaresize
        return (r,c)

    #use the game state to update the baord GUI
    def updateStones(self):

        for point in self.gamestate.boardState:
            
            r,c = point[0],point[1]

            #last = (point == self.last)
            
            if((r,c) in self.stoneIDs):
                self.board.delete(self.stoneIDs[(r,c)])

            if (self.gamestate.boardState[point] == gamestate.STONE):
                self.stoneIDs[(r,c)] = self.drawStone( (r,c) , False)
            elif (self.gamestate.boardState[point] == gamestate.BALL):
                self.stoneIDs[(r,c)] = self.drawStone( (r,c), True)


    def toggleJumping(self):

        if(self.jumping):
            self.gamestate = self.jumpingState
            self.jumpingState = None
        else:
            self.initJumpingObjects()

        self.jumping = not self.jumping

    #initialize the extra stuff to handle jump moves
    def initJumpingObjects(self):
        self.jumpingState = self.gamestate.copy()


    #called on a click
    def onClick(self,event):

        if not self.clickable: return

        r,c = self.row_col(event.x,event.y)

        if (r,c) == self.gamestate.ball:
            self.toggleJumping()
        elif self.jumping:
            if self.jumpingState.boardState[(r,c)] == gamestate.EMPTY:
                if (r,c) in self.jumpingState.legalJumpSquares():
                    self.jumpingState.jumpTo((r,c))
                    self.toggleJumping()
                    self.updateStones()

        else:
            success = self.tryPlace(r,c)
            if(success):
                #self.nextTurn()
                pass



    #try to place a stone
    #fails if spot is taken or if it's out of bounds
    def tryPlace(self,r,c):
        if r<0 or r>self.rows-1 or c<0 or c>self.cols-1:
            return False
        if self.gamestate.boardState[(r,c)] != gamestate.EMPTY:
            return False
        self.gamestate.setStone((r,c))

        #self.last = (r,c) #new
                   
        self.updateStones()
        return True
        
    #called when the cursor moves
    # def onMove(self,event):

    #     if not self.clickable: return
        
    #     r,c = self.row_col(event.x,event.y)
    #     if r<0 or r>self.rows-1 or c<0 or c>self.cols-1:
    #         if(self.cursorStoneId != -1): #copy pasta
    #             self.board.delete(self.cursorStoneId)
    #             self.cursorStoneId = -1
    #         return
    #     if(r != self.cursorRow or c != self.cursorCol):
    #         if(self.cursorStoneId != -1):
    #             self.board.delete(self.cursorStoneId)
    #         if(self.gamestate.stones[(r,c)] == 0): #empty square
    #             if(self.gamestate.p1Turn):
    #                 color = "#FFCCCC"
    #             else:
    #                 color = "#CCFFFF"
    #             self.cursorStoneId = self.drawStone(r,c,color,False)
    #             self.cursorRow, self.cursorCol = r,c
    #         else:
    #             self.cursorRow, self.cursorCol = -1,-1
        
    #create stone, return ID
    def drawStone(self, coords, football=False):
        r,c = coords
        center = (self.hborder + c*self.squaresize, self.vborder + r*self.squaresize)
        color = "black" if football else "white"
        rad = self.stonerad
        return self.board.create_oval(center[0]-rad, center[1]-rad,center[0]+rad,center[1]+rad, fill=color, width = 1, outline = "black")

    #wait for a move 
    def acceptMove(self):
        self.clickable = True

    #def onMove(self, event):
    #    pass



    def __init__(self, parent, gamestate):
        
        tk.Frame.__init__(self,parent)
        self.gamestate = gamestate
        self.rows = self.gamestate.rows #number of horizontal lines
        self.cols = self.gamestate.cols #number of vertical lines
        self.hborder = 50 #left-right border
        self.vborder = 20 #top-bottom border
        self.squaresize = 35
        self.stonerad = 0.3*self.squaresize
        w = (self.cols-1)*self.squaresize + 2*self.hborder
        h = (self.rows-1)*self.squaresize + 2*self.vborder

        self.stoneIDs = {} #keep track of stone id's 


        self.board = tk.Canvas(parent, width=w, height=h)
        self.board.pack()

        self.jumping = False



        self.clickable = True #can the player click on the screen?

        for i in range(0,self.cols):
            x = self.hborder+i*self.squaresize
            self.board.create_line(x,self.vborder,x,self.vborder+self.squaresize*(self.rows-1))
    
        for i in range(0,self.rows):
            y = self.vborder+i*self.squaresize
            self.board.create_line(self.hborder,y,self.hborder+self.squaresize*(self.cols-1),y)

        
        self.board.bind("<Button-1>", self.onClick)
        #self.board.bind("<Motion>", self.onMove)

        self.updateStones()
        #self.nextTurn() #start the game

top = tk.Tk()
state = gamestate.GameState()
board = Board(top, state)
top.mainloop()
