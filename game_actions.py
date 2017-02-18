from holding_area import holding_area

class AbstractAction(object):
    pass


class PrintAction(AbstractAction):
    def __init__(self, text):
        self.text = text

    def activate(self):
        print(self.text)


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


class BuyCard(AbstractAction):
    # Pay cost
    # Move card
    def __init__(self, card, player):
        self.card = card
        self.player = player

    def activate(self):
        pass

class TakeChip(AbstractAction):
    """
    The current player takes a chip:
    move a chip from this chip stack to the holding area
    """
    def __init__(self, chip_stack):
        self.chip_stack = chip_stack

    def activate(self, current_player):
        """
        :param current_player:
        :return:
        """

        # Move chip from supply to holding area
        self.chip_stack.take_one()
        holding_area.add_chip(self.chip_stack.chip)
        current_player.take_component()
        return True
