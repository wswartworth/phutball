import random
import math
import time
import copy

class MCGameTreeNode:
    #need to set the player for the root node
    def __init__(self, parent, gamestate, depth):
        #print("New node: ", depth)
        self.parent = parent
        self.childMoves = {} #maps moves to children
        self.depth = depth

        if(self.parent != None):
            self.player = -1 * self.parent.player
        
        #self.move = move #the move used to get to this node
        self.gamestate = gamestate
        self.p1Wins = 0
        self.p2Wins = 0 
        self.lastScore = None #only for debugging 

    def newChildNode(self, move):
        newState = self.gamestate.copy()
        newState.makeMove(move)
        newChild = MCGameTreeNode(self, newState, self.depth+1)
        self.childMoves[move] = newChild
        return newChild

    # def winUpdate(self,winner):
    #     if winner == 1:
    #         self.p1Wins = self.p1Wins + 1
    #         return
    #     if winner == -1:
    #         self.p2Wins = self.p2Wins + 1
    #         return
    #     if winner == 0:
    #         self.p1Wins = self.p1Wins + 0.5
    #         self.p2Wins = self.p2Wins + 0.5
    #         return

    # def down(self,move):
    #     assert move in self.curNode.childMoves
    #     return self.childMoves[move]
    #     #else:
    #     #    newNode = MCGameTreeNode(self.curNode,move)
    #     #    self.curNode.childMoves[move] = newNode
    #     #    self.curNode = newNode
    #     #self.gamestate.makeMove(move)

    def printDescendents(self, depth):
        print(depth * "    ", "[", self.p1Wins, " ", self.p2Wins, "]", "  :: ", self.lastScore)
        for m in self.childMoves:
            self.childMoves[m].printDescendents(depth+1)

    #matters whose turn it is
    def score(self):

        t = self.parent.p1Wins + self.parent.p2Wins #total simulations involving parent
        lastPlayer = -1*self.player

        if(lastPlayer == 1): #CHANGED
            wins = self.p1Wins
        else:
            wins = self.p2Wins

        n = self.p1Wins + self.p2Wins
        C = 1.5 #EXPLORATION CONSTANT

        assert n != 0, "attempt to score unexplored node"

        s = (wins/n) + C * math.sqrt(math.log(t)/n)

        self.lastScore = s

        return s #the "suggested" function

    def selectBestDescendent(self):

        if(len(self.childMoves) == 0): return self

        bestScore = -float("inf")
        bestChild = None
        for move in self.childMoves:
            childNode = self.childMoves[move]
            childScore = childNode.score() #need to fix score()
            if childScore > bestScore:
                bestScore = childScore
                bestMove = move

        return self.childMoves[bestMove].selectBestDescendent()




        # while(True):
        #     curPlayer = self.gamestate.curPlayer()
        #     bestScore = -float("inf")
        #     bestMove = None
        #     children = self.curNode.childMoves
        #     if(len(children) != len(self.gamestate.empty) ): #there are unexplored children
        #     #EXPAND EVERYTHING?
        #         return
            
        #     for move in self.curNode.childMoves:
        #         childNode = self.curNode.childMoves[move]
        #         childScore = childNode.score(self.curNode.p1Wins + self.curNode.p2Wins)
        #         if childScore > bestScore:
        #             bestScore = childScore
        #             bestMove = move
        #     if(bestMove != None):
        #         self.down(bestMove)
        #     else:
        #         return

    def backProp(self, p1Update, p2Update):

        self.p1Wins += p1Update
        self.p2Wins += p2Update

        if self.parent == None:
            return
        else: 
            self.parent.backProp(p1Update, p2Update)


            #self.updateWinCount(p1Wins,p2Wins)
                
            #if(self.curNode.parent != None):
            #    self.up()
            #else:
            #    return
        

#changes gamestate
def softPlayout(gamestate):
    #print("        start playout      ")

    winner = None

    #i = 0

    #print("winner: ", gamestate.getWinner)
    while gamestate.getWinner() == None:

        legalMoves = gamestate.legalMoves()
        if(len(legalMoves) == 0): 
            break

        randMove = random.choice(legalMoves)
        gamestate.makeMove(randMove)
        #print(randMove)

    #print("State:", gamestate.boardState)

    if(gamestate.getWinner() == None): 
        #print("winner: no winner")
        return 0
    else: 
        #print("winner: ", gamestate.getWinner())
        return gamestate.getWinner()

    

def MCiteration(root):
        #root.printDescendents(0)
        node = root.selectBestDescendent()
        moves = node.gamestate.legalMoves()
        p1Wins = 0
        p2Wins = 0

        #How to handle this case?
        if node.gamestate.winner == 1:
            p1Wins = 1
            node.backProp(10,0)  #testing code
        elif node.gamestate.winner == -1:
            p2Wins = 1
            node.backProp(0,10)
                
        for m in moves:

            child = node.newChildNode(m)
            winner = softPlayout(child.gamestate.copy())
            #print("winner: ", winner)
            if winner == 0: 
                p1Wins, p2Wins = 0.5, 0.5
            if winner == 1: 
                p1Wins, p2Wins = 1, 0
            if winner == -1: 
                p1Wins, p2Wins = 0, 1

            child.backProp(p1Wins, p2Wins)
            

def getAIMove(gamestate, iterations):

    root = MCGameTreeNode(None, gamestate, 0)
    root.player = 1 if gamestate.p1Turn else -1

    for i in range(0,iterations): 
        if(i % 500 == 0): print(i)
        MCiteration(root)

    bestMove = None
    curMax = 0

    for m in root.childMoves: #This could probably be more pythonic
        node = root.childMoves[m]
        numVisited = node.p1Wins + node.p2Wins
        if(numVisited > curMax):
            curMax = numVisited
            bestMove = m

    #root.printDescendents(0)
  
    return bestMove
    
#creates the abstraction of a full game tree stored in memory which can be accessed
# class MCGameTree:    
#     #gamestate gets updated as we move up and down the tree
#     def __init__(self, gamestate, iterations):
#         #self.gamestate = gamestate
#         self.root = MCGameTreeNode(None, None)
#         self.root.player = 1 #set!
#         self.curNode = self.root
#         self.iterations = iterations

#     # def up(self):
#     #     self.gamestate.undo(self.curNode.move)
#     #     self.curNode = self.curNode.parent
        
#     #     if(self.curNode == None):
#     #         print("tried to access parent of root")

#     #go down the tree until finding unexplored moves
#     # def selectNewNode(self):
#     #     while(True):
#     #         curPlayer = self.gamestate.curPlayer()
#     #         bestScore = -float("inf")
#     #         bestMove = None
#     #         children = self.curNode.childMoves
#     #         if(len(children) != len(self.gamestate.empty) ): #there are unexplored children
#     #             #EXPAND EVERYTHING?
#     #             return
            
#     #         for move in self.curNode.childMoves:
#     #             childNode = self.curNode.childMoves[move]
#     #             childScore = childNode.score(self.curNode.p1Wins + self.curNode.p2Wins)
#     #             if childScore > bestScore:
#     #                 bestScore = childScore
#     #                 bestMove = move
#     #         if(bestMove != None):
#     #             self.down(bestMove)
#     #         else:
#     #             return


#     # def printMovePath(self):
#     #     while(True):
#     #         curPlayer = self.gamestate.curPlayer()
#     #         bestScore = -float("inf")
#     #         bestMove = None
#     #         children = self.curNode.childMoves
            
#     #         for move in self.curNode.childMoves:
#     #             childNode = self.curNode.childMoves[move]
#     #             childScore = childNode.score(self.curNode.p1Wins + self.curNode.p2Wins)
#     #             if childScore > bestScore:
#     #                 bestScore = childScore
#     #                 bestMove = move
#     #         if(bestMove != None):
#     #             print("move: ", bestMove)
#     #             self.down(bestMove)
#     #         else:
#     #             while(self.curNode.parent != None): self.up()
#     #             return
        
    
#     #explores a totally random child node
#     # def MCRandomExplore(self):
#     #     numMoves = len(self.gamestate.empty)
        
#     #     if self.gamestate.winner != 0:
#     #         return #don't try to explore for a winning position
        
#     #     if numMoves == 0: return #other things we could do...
        
#     #     #Might want to make sure that this function does choose something that's already in the tree

#     #     randMove = None
#     #     while((randMove==None) or (randMove in self.curNode.childMoves)): #Really stupid!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     #         randMove = self.gamestate.empty[random.randint(0,numMoves - 1)] #just use random choice
#     #     self.down(randMove)

#     # def MCExploreAll(self):
#     #     if self.gamestate.winner != 0:
#     #         return []
#     #     return copy.copy(self.gamestate.empty) #need to copy?
        

#     # def updateWinCount(self,p1Wins, p2Wins):
#     #     self.curNode.p1Wins  = self.curNode.p1Wins + p1Wins
#     #     self.curNode.p2Wins = self.curNode.p2Wins + p2Wins
    
#     #assumes that self.curNode is the state that winner corresponds to


#     #playout with uniformly random moves
#     # def softPlayout(self, gamestate):

#     #     winner = None
#     #     while gamestate.getWinner == None:
#     #         legalMoves = gamestate.legalMoves()
#     #         if(len(legalMoves) == 0): return 0

#     #         randMove = random.choice(legalMoves)
#     #         gamestate.makeMove(randMove)
#     #         winner = gamestate.newWinner(randMove)
#     #         if winner != None: break

#     #     return winner


    
#     def MCiteration(self):
#         self.newMCSelectNode()
#  #       print("selected: ", self.curNode.move)
#  #       self.root.printDescendents(0)
#   #      self.MCRandomExplore()
#         moves = self.MCExploreAll()
#         p1Wins = 0
#         p2Wins = 0
# #        print("random child: ", self.curNode.move)

#         if self.gamestate.winner == 1:
#             p1Wins = 1
#         elif self.gamestate.winner == -1:
#             p2Wins = 1
                
#         for m in moves:
#             #self.down(m) #FIX
            
#             newState = self.gamestate.copy()
#             newState.makeMove(m)
#             winner = self.playout(newState)

#             p1Inc = 0
#             p2Inc = 0
#             if winner == 1:
#                 p1Inc = p1Inc+1
#             elif winner == -1:
#                 p2Inc = p2Inc + 1
#             elif winner == 0:
#                 p1Inc = p1Inc + 0.5
#                 p2Inc = p2Inc + 0.5
#             p1Wins = p1Wins + p1Inc
#             p2Wins = p2Wins + p2Inc
#             self.updateWinCount(p1Inc,p2Inc)
#             #self.up()
            
#         self.backProp(p1Wins, p2Wins)
           
#     def getAIMove(self):
#         #start = time.time()
#         for i in range(0,self.iterations):
#             #if(i % 100 == 0): print(i)
#             self.MCiteration()
#  #       self.root.printDescendents(0)

#         bestMove = None
#         curMax = 0
#         for m in self.root.childMoves:
#             node = self.root.childMoves[m]
#             numVisited = node.p1Wins + node.p2Wins
#             if(numVisited > curMax):
#                 curMax = numVisited
#                 bestMove = m
#         #end = time.time()
#         #print("AI time: ", end-start)
        
# #        self.printMovePath()
#  #       self.root.printDescendents(0)
        
#         return bestMove


#     def makeMove(self,move):
#  #       self.gamestate.makeMove(move)
#         self.root = MCGameTreeNode(None, None)
#         self.root.player = self.gamestate.curPlayer() #set!
#         self.curNode = self.root


import connectFourGamestate as connectFourGamestate

state = connectFourGamestate.GameState(6,7)
while(True):
    move = getAIMove(state,5000)
    print("Move choice: ", move)
    state.makeMove(move)
    inMove = int(input())
    state.makeMove(inMove)


