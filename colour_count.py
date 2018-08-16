from utils import chip_type_for_colour_name
from util_classes import ChipType

from embody import EmbodyChipStackMixin, EmbodyChipCostMixin, \
    EmbodyPlayerChipStack, EmbodyPlayerCardStack


class ColourCount:
    """
    Maintain a count of chips by type (colour), or of cards by chip type
     they 'produce'
    """

    def __init__(self, colour_count=None, raw_colour_count=None):
        """
        :param colour_count: Number of chips/cards by type
        :type colour_count: dict(chip_type: count)
        :param str raw_colour_count: Colour count as a string, e.g '5 red, 3 blue'
        """
        if colour_count is not None:
            self.colour_count = colour_count
        elif raw_colour_count is not None:
            self.colour_count = {}
            for c in raw_colour_count.split(','):
                chip_count, chip_colour = c.strip().split(' ')
                self.colour_count[chip_type_for_colour_name(chip_colour)] \
                    = int(chip_count)

    def filter(self, remove_blanks=False):
        """
        Different way(s) to filter down the colour count

        :param bool remove_blanks: If True, remove any dict keys with 0 value
        :return: if remove_blanks, colour count for non-zero values, else original colour count
        :rtype: ColourCount
        """
        result = self

        if remove_blanks:
            result = self.__class__(
                {k: v for k, v in self.colour_count.items() if v != 0}
            )

        return result

    def __len__(self):
        return len(self.colour_count)

    def __contains__(self, item):
        return item in self.colour_count

    def __iter__(self):
        return iter(self.colour_count.keys())

    def items(self):
        """
        :return: list(key:value) of the colour count
        """
        return self.colour_count.items()

    def covers_cost(self, chip_cost):
        """
        Do the chips we've counted cover the cost specified.
        Yellow chips are used as wild cards

        :param chip_cost: The cost to cover
        :type chip_cost: ColourCount
        :return: True, if this covers the cost
        :rtype: bool
        """

        # How many chips are we short
        yellow_needed = sum(
            max(chip_cost.colour_count[chip_type]
                - self.colour_count[chip_type], 0)
            for chip_type in chip_cost.colour_count
            if chip_type is not ChipType.yellow_gold
        )

        # Have we got enough chips to cover any shortage
        return self.colour_count[ChipType.yellow_gold] >= yellow_needed


class ChipStacks(ColourCount, EmbodyChipStackMixin):
    """
    A ColourCount subclass which can be shown as a stack of chips
    in the supply
    """
    pass


class ChipCost(ColourCount, EmbodyChipCostMixin):
    """
    A ColourCount subclass which can be shown on a card as its cost
    """
    pass


class PlayerChipStack(ColourCount, EmbodyPlayerChipStack):
    """
    A ColourCount subclass which can be shown as a stack of chips
    for a player
    """
    pass


class PlayerCardStack(ColourCount, EmbodyPlayerCardStack):
    """
    A ColourCount subclass representing the 'reward' (in chip count)
    given by a player's cards
    """
    pass
