class AbstractAction(object):
    pass


class MoveComponent(AbstractAction):
    # Move chip
        # from supply to target_player
        # from source_player to supply
    # Move tile1
        # from supply to target_player
    # Move card
        # from supply to target_player's hand
        # from supply to target_player's reserve area
        # from draw pile to supply

    def __init__(self):
        pass

    def activate(self):
        pass


class PayCost(AbstractAction):
    def __init__(self, item, player):
        self.item = item
        self.player = player

    def activate(self):
        pass


class TakeCard(AbstractAction):
    # Pay cost
    # Move card
    def __init__(self, card, holding_area):
        self.card = card
        self.holding_area = holding_area

    def activate(self, current_player):
        self.card.source.card = None
        self.holding_area.card = self.card
        current_player.take_component()
        return ['refresh_display']


def return_card(holding_area, card):
    card.source.card = card
    holding_area.card = None


class ReturnCard(AbstractAction):
    def __init__(self, card, holding_area):
        self.card = card
        self.holding_area = holding_area

    def activate(self, current_player):
        return_card(self.holding_area, self.card)
        current_player.return_component()
        return ['refresh_display']


class TakeChip(AbstractAction):
    """
    The current player takes a chip:
    move a chip from this chip stack to the holding area
    """
    def __init__(self, chip, holding_area):
        self.chip = chip
        self.holding_area = holding_area

    def activate(self, current_player):
        """
        :param current_player:
        :return:
        """

        # Move chip from supply to holding area
        # self.chip_stack.take_one()
        self.chip.source.take_chip(self.chip)
        self.holding_area.add_chip(self.chip)
        current_player.take_component()
        return ['refresh_display']


# def return_chip(holding_area, chip):
#     holding_area.remove_chip(chip)
#     chip.source.add_one()


class ReturnChip(AbstractAction):
    """

    """
    def __init__(self, chip, holding_area):
        self.chip = chip
        self.holding_area = holding_area

    def activate(self, current_player):
        return_chip(self.holding_area, self.chip)
        current_player.return_component()
        return ['refresh_display']


class Confirm(AbstractAction):
    def __init__(self, holding_area):
        self.holding_area = holding_area

    def activate(self, current_player):
        self.holding_area.chips.transfer_chips(current_player.chips)
        # for chip in self.holding_area.chips:
        #     self.holding_area.remove_chip(chip)
        #     current_player.add_chip(chip)

        if self.holding_area.card:
            card = self.holding_area.card
            current_player.pay_cost(card.chip_cost)

            # Draw a new card and assign it to the original card's slot
            current_player.add_card(card)
            card.source.card = card.card_deck.pop()
            card.source.card.source = card.source

            self.holding_area.card = None

        return ['next_player', 'refresh_display']


class Cancel(AbstractAction):
    def __init__(self, holding_area):
        self.holding_area = holding_area

    def activate(self, current_player):
        self.holding_area.chips.return_chips()
        # for chip in self.holding_area.chips:
        #     return_chip(self.holding_area, chip)

        if self.holding_area.card:
            return_card(self.holding_area, self.holding_area.card)

        current_player.cancel()
        return ['refresh_display']
