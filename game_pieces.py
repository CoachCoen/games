from enum import Enum

class JewelType(Enum):
    green_emerald = 1
    blue_sapphire = 2
    red_ruby = 3
    white_diamond = 4
    black_onyx = 5
    yellow_gold = 6

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
