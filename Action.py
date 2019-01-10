
from ActionTypes import ActionTypes


class Action:

    def __init__(self, actionType, coordinates):
        assert type(actionType) is ActionTypes
        assert type(coordinates) is list

        self.type = actionType
        self.coordinates = list(coordinates)

    def appendCoordinate(self, coordinate):
        self.coordinates.append(coordinate)
