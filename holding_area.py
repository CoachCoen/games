from settings import Vector, config
from drawing_surface import draw_rectangle, ColourPalette

class HoldingArea(object):
    """
    During a player's turn, holds the items which
    the player has selected, before they confirm this
    """
    def __init__(self):
        self.chips = []
        self.card = None
        self.location = None

    def clear(self):
        self.__init__()

    def add_chip(self, chip):
        self.chips.append(chip)

    def embody(self, location):
        if not self.chips and not self.card:
            return
        self.location = location
        self._draw()
        self.location = location
        for i, chip in enumerate(self.chips):
            chip.embody(
                self.location +
                Vector((i * 2.5 + 2) * config.chip_size, 2 * config.chip_size),
            )

    def _draw(self):
        draw_rectangle(self.location.to_rectangle(config.holding_area_size),
                       ColourPalette.holding_area)

holding_area = HoldingArea()
