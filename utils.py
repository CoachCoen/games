from util_classes import ChipType
from game_components import Chip


def chip_type_for_colour_name(colour_name):
    """
    Convert a string (colour) to a ChipType

    :param str colour_name: colour, e.g. 'red'
    :return: the ChipType for this colour
    """
    return {
        'red': ChipType.red_ruby,
        'blue': ChipType.blue_sapphire,
        'white': ChipType.white_diamond,
        'green': ChipType.green_emerald,
        'black': ChipType.black_onyx,
        'yellow': ChipType.yellow_gold
    }[colour_name]


def pieces_match(a, b):
    """
    Are a and b either the same piece or the same colour of chip

    :param a: A game component
    :type a: game_components.AbstractGameComponent
    :param b: Another game component
    :type b: game_components.AbstractGameComponent
    :return: True if A and B match
    """

    if a == b:
        return True
    return isinstance(a, Chip) \
        and isinstance(b, Chip) \
        and a.chip_type == b.chip_type


class SplitIntoIncludedAndExcluded:
    """
    Split up pieces in source and target:

    * self.included: both in source + target
    * self.excluded: in target but not in source
    * self.remaining: in source but not in target

    Chips of the same colour are treated as the same piece.
    Unlike sets, the lists can contain multiple pieces of the same type.
    This is typically used to work out whether a player can take
    a piece, halfway through a turn, based on the list of available moves
    """

    def __init__(self, source, target):
        self.included = []
        self.excluded = []
        self.remaining = source[:]
        for target_piece in target:
            found = False
            for i, remaining_piece in enumerate(self.remaining):
                if not found and pieces_match(target_piece, remaining_piece):
                    self.included.append(remaining_piece)
                    del (self.remaining[i])
                    found = True
            if not found:
                self.excluded.append(target_piece)
