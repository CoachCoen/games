from utils import chip_type_for_colour_name
from embody import EmbodyChipStackMixin, EmbodyChipCostMixin, EmbodyPlayerChipStack
from chip_types import ChipType

class ColourCount():
    def __init__(self, colour_count=None, raw_colour_count=None):
        if colour_count is not None:
            self.colour_count = colour_count
        elif raw_colour_count is not None:
            self.colour_count = {}
            for c in raw_colour_count.split(','):
                chip_count, chip_colour = c.strip().split(' ')
                self.colour_count[chip_type_for_colour_name(chip_colour)] \
                    = int(chip_count)

    def filter(self, remove_blanks=False):
        result = self

        if remove_blanks:
            result = self.__class__({k: v for k, v in self.colour_count.items() if v != 0})

        return result

    def __len__(self):
        return len(self.colour_count)

    def __contains__(self, item):
        return item in self.colour_count

    def __iter__(self):
        return iter(self.colour_count.keys())

    def items(self):
        return self.colour_count.items()

    def covers_cost(self, chip_cost):
        # Cover any missing chips/cards with yellow chips
        yellow_needed = sum(
            max(chip_cost.colour_count[chip_type] - self.colour_count[chip_type], 0)
            for chip_type in chip_cost.colour_count
            if chip_type is not ChipType.yellow_gold
        )
        return self.colour_count[ChipType.yellow_gold] >= yellow_needed


class ChipStacks(ColourCount, EmbodyChipStackMixin):
    pass


class ChipCost(ColourCount, EmbodyChipCostMixin):
    pass


class PlayerChipStack(ColourCount, EmbodyPlayerChipStack):
    pass
