from settings import Vector, config
from drawing_surface import draw_rectangle, ColourPalette
from buttons import buttons
from game_actions import Cancel, Confirm
from game_state import game_state


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

    def remove_chip(self, chip):
        self.chips = [c for c in self.chips if c is not chip]

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
                can_click=True
            )
        if self.card:
            self.card.embody(
                self.location + config.holding_area_card_location,
                can_return=True
            )

        buttons.add(
            (self.location + config.cancel_button_location).
                to_rectangle(config.button_size),
            Cancel(holding_area),
            text='Cancel'
        ).embody()

        if game_state.is_turn_complete:
            buttons.add(
                (self.location + config.confirm_button_location)
                    .to_rectangle(config.button_size),
                Confirm(holding_area),
                text='Confirm'
            ).embody()

    def _draw(self):
        draw_rectangle(self.location.to_rectangle(config.holding_area_size),
                       ColourPalette.holding_area)

    def is_empty(self):
        return not self.card and not self.chips

holding_area = HoldingArea()
