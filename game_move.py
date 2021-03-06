from enum import Enum


class MoveType(Enum):
    take_different_chips = 1
    take_same_chips = 2
    buy_card = 3
    reserve_card = 4
    take_tile = 5


class Move:
    def __init__(self, pieces, move_type, required=None):
        self.pieces = pieces
        self.move_type = move_type
        self.required = required if required is not None else []
