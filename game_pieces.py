from enum import Enum
from data import JewelType

class AbstractGamePiece(object):
    pass

class NobelsTile(AbstractGamePiece):
    def __init__(self, cost, points):
        self.cost = cost
        self.points = points

class Chip(AbstractGamePiece):
    def __init__(self, jewel_type):
        self.jewel_type = jewel_type

class Card(AbstractGamePiece):
    def __init__(self, cost, jewel_type, row, points=0):
        self.cost = cost
        self.jewel_type = jewel_type
        self.points = points
        self.row = row
