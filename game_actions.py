from game_state import game
from component_states import ComponentState


class AbstractAction(object):
    pass


class TakeCard(AbstractAction):
    def __init__(self, card):
        self.card = card

    def activate(self):
        if self.card.position == ComponentState.card_grid:
            game.table.card_grid.take_card(self.card)
        elif self.card.position == ComponentState.reserved:
            game.current_player.reserved.take_card(self.card)
        game.holding_area.card = self.card
        if game.current_player.is_human:
            game.current_player.take_component()
        return True


class ReturnCard(AbstractAction):
    def __init__(self, card):
        self.card = card

    def activate(self):
        game.table.card_grid.return_card(self.card)
        game.holding_area.card = None
        game.current_player.return_component()
        return True


class TakeChip(AbstractAction):
    """
    The current player takes a chip:
    move a chip from this chip stack to the holding area
    """
    def __init__(self, chip):
        self.chip = chip

    def activate(self):
        """
        :return:
        """

        # Move chip from supply to holding area
        game.table.chips.take_chip(self.chip)
        game.holding_area.add_chip(self.chip)
        # if game.current_player.is_human:
        if not game.AI_move:
            game.current_player.take_component()
        return True


class ReturnChip(AbstractAction):
    def __init__(self, chip):
        self.chip = chip

    def activate(self):
        self.chip.return_to_supply()
        game.holding_area.chips.take_chip(self.chip)
        game.current_player.return_component()
        return True


class Confirm(AbstractAction):
    @staticmethod
    def activate():
        game.current_player.confirm()
        return True


class Cancel(AbstractAction):
    @staticmethod
    def activate():
        game.current_player.cancel()
        return True
