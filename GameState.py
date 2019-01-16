
from Action import Action
from ActionTypes import ActionTypes
from BoardStates import BoardStates


# empty should really be a set
class GameState():

    neighborDelta = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    def __init__(self, rows=19, cols=15):

        self.rows = rows
        self.cols = cols
        self.p1Turn = True
        self.ball = (self.rows//2, self.cols//2)
        self.boardDelta = dict()
        self.boardState = {}

        # initalize the board to be empty with a ball in the middle
        for i in range(0, rows):
            for j in range(0, cols):
                self.boardState[(i, j)] = BoardStates.Empty

        self.boardState[self.ball] = BoardStates.Ball

    def applyAction(self, action: Action):

        assert type(action) is Action

        if action.type is ActionTypes.SetStone:
            self.setStone(action.coordinates)
        elif action.type is ActionTypes.MoveBall:
            self.moveBall(action.coordinates)
        else:
            assert False, "Invalid action type"

    def canMoveBall(self):

        ballPosition = self.getBallPosition()

        for dr, dc in GameState.neighborDelta:
            neighbor = (ballPosition[0] + dr, ballPosition[1] + dc)
            if (not self.inBounds(neighbor)):
                continue

            if (self.getStateAtPosition(neighbor) is BoardStates.Stone):
                return True

        return False

    def getAllPositions(self):

        return self.boardState.keys()

    def getBoardDelta(self):

        return self.boardDelta

    def getBallPosition(self):

        return self.ball

    def getInBetweenPositions(self, start, end):

        changeR = end[0] - start[0]
        changeC = end[1] - start[1]

        normChangeR = changeR if changeR == 0 else changeR/abs(changeR)
        normChangeC = changeC if changeC == 0 else changeC/abs(changeC)

        maxDifference = max(abs(changeR),  abs(changeC))

        positions = list()
        for i in range(1, int(maxDifference)):
            positions.append((start[0] + normChangeR * i, start[1] + normChangeC * i))

        return positions

    def getStateAtPosition(self, position):

        return self.boardState[position]

    def getStonePositions(self):

        return [coordinate for coordinate in self.boardState if self.boardState[coordinate] is BoardStates.Stone]

    def inBounds(self, coords):

        r, c = coords[0], coords[1]
        return (0 <= r <= self.rows-1) and (0 <= c <= self.cols-1)

    def moveBall(self, coordinates):

        # self.validateMoveBall(coordinates)
        self.boardDelta = dict()

        currentBallPosition = self.getBallPosition()
        newBallPosition = coordinates[0]

        # Get positions in between the two ball positions
        inbetween = self.getInBetweenPositions(currentBallPosition, newBallPosition)

        for position in inbetween:
            self.boardState[position] = BoardStates.Empty
            self.boardDelta[position] = BoardStates.Empty

        self.boardState[currentBallPosition] = BoardStates.Empty
        self.boardDelta[currentBallPosition] = BoardStates.Empty

        self.boardState[newBallPosition] = BoardStates.Ball
        self.boardDelta[newBallPosition] = BoardStates.Ball

        self.ball = newBallPosition

    def setStone(self, coordinates):

        self.validateSetStone(coordinates)
        self.boardDelta = dict()

        self.boardState[coordinates[0]] = BoardStates.Stone
        self.boardDelta[coordinates[0]] = BoardStates.Stone

    def validateMoveBall(self, coordinates: list):

        assert len(coordinates) > 2, "MoveBall action requires at least 2 coordinate pairs"
        assert self.boardState[coordinates[0]] == BoardStates.Ball, "MoveBall action must start with ball"

        for point in coordinates[1:-1]:
            assert self.boardState[point] == BoardStates.Stone, "Ball must just over stones"

        assert self.boardState[coordinates[-1]] == BoardStates.Empty, "Ball must land in empty position"

    def validateSetStone(self, coordinate: list):

        assert len(coordinate) == 1, "SetStone action takes only one coordinate pair"
        assert (self.boardState[coordinate[0]] == BoardStates.Empty), "Stone can only be placed on an empty position"
