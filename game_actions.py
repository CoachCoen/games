from game_state import game
from chip_types import ChipType
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
        game.current_player.take_component()
        return True


def return_card(card):
    game.table.card_grid.return_card(card)
    game.holding_area.card = None


class ReturnCard(AbstractAction):
    def __init__(self, card):
        self.card = card

    def activate(self):
        return_card(self.card)
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
        game.current_player.take_component()
        return True


def return_chip(chip):
    chip.return_to_supply()
    game.holding_area.chips.take_chip(chip)


class ReturnChip(AbstractAction):
    """

    """
    def __init__(self, chip):
        self.chip = chip

    def activate(self):
        return_chip(self.chip)
        game.current_player.return_component()
        return True


class Confirm(AbstractAction):
    @staticmethod
    def activate():
        held_card = game.holding_area.card

        if game.holding_area.chips.any_chip_of_type(ChipType.yellow_gold):
            # Yellow chip taken, so reserved card
            game.current_player.reserve_card(held_card)
            game.table.card_grid.fill_empty_spaces()

        elif held_card:
            # Take card
            game.current_player.pay_cost(held_card.chip_cost)

            # Draw a new card and assign it to the original card's slot
            game.current_player.add_card(held_card)
            game.table.card_grid.fill_empty_spaces()
            # card.source.card = game.table.card_deck.pop()
            # card.source.card.source = card.source

        game.holding_area.card = None

        game.holding_area.chips.transfer_chips(game.current_player.chips)
        game.next_player()

        return True


class Cancel(AbstractAction):
    @staticmethod
    def activate():
        game.holding_area.chips.return_chips()

        if game.holding_area.card:
            return_card(game.holding_area.card)

        game.current_player.cancel()
        return True
