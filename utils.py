from util_classes import ChipType
from game_components import Chip


def chip_type_for_colour_name(colour_name):
    return {
        'red': ChipType.red_ruby,
        'blue': ChipType.blue_sapphire,
        'white': ChipType.white_diamond,
        'green': ChipType.green_emerald,
        'black': ChipType.black_onyx,
        'yellow': ChipType.yellow_gold
    }[colour_name]


def pieces_match(a, b):
    if a == b:
        return True
    return isinstance(a, Chip) and isinstance(b, Chip) and a.chip_type == b.chip_type


class SplitIntoIncludedAndExcluded:
    def __init__(self, source, target):
        self.included = []              # pieces which are both in source + target
        self.excluded = []              # pieces which are in target but not in source
        self.remaining = source[:]      # pieces which are in source but not in target
        for target_piece in target:
            found = False
            for i, remaining_piece in enumerate(self.remaining):
                if not found and pieces_match(target_piece, remaining_piece):
                    self.included.append(remaining_piece)
                    del (self.remaining[i])
                    found = True
            if not found:
                self.excluded.append(target_piece)
