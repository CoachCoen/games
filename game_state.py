from data import ChipType

def get_is_turn_complete():
    holding_area = game_state.game.holding_area
    # 2 of same chip selected
    if len(holding_area.chips) == 2 \
            and holding_area.chips.different_types == 1:
        return True

    # 3 different chips selected
    if len(holding_area.chips) == 3:
        return True

    # 1 card selected
    if holding_area.card:
        return True

    # No chips left to take
    # TODO: Fix/Test this
    if not holding_area.chips.empty \
            and not game_state.game.table.chips.any_non_yellow_chips:
        return True

    return False


def get_valid_actions():
    if game_state.is_turn_complete:
        return []

    holding_area_chips = game_state.game.holding_area.chips
    table_chips = game_state.game.table.chips

    valid_actions = []

    # Which chips can be selected?
    for chip_type in ChipType:
        chip = table_chips.first_chip_of_type(chip_type)

        # No chip of this type in the supply
        if not chip:
            continue

        # If yellow selected, can't select any other chips
        if holding_area_chips.any_chip_of_type(ChipType.yellow_gold):
            continue

        # If any (non-yellow) chip selected, can't select yellow chip
        if not holding_area_chips.empty \
                and chip_type == ChipType.yellow_gold:
            continue

        # If already selected 2 chips, can't select a colour again
        if len(holding_area_chips) == 2 and \
                holding_area_chips.any_chip_of_type(chip_type):
            continue

        # If already selected 1 chip, can't select that colour again if
        # this are 2 or less chips of that colour (not counting the one
        # already selected)
        if len(holding_area_chips) == 1 \
                and holding_area_chips.any_chip_of_type(chip_type) \
                and table_chips.count(chip_type) <= 2:
            continue

        valid_actions.append(
            game_state.game.table.chips.first_chip_of_type(chip_type)
        )

    # Which cards can be selected?
    # TODO: More Pythonic way to loop through this?
    for row in game_state.game.table.card_grid:
        for card_slot in row:
            card = card_slot.card
            if not card:
                continue

            # If yellow chip picked, can select all
            if holding_area_chips.any_chip_of_type(ChipType.yellow_gold):
                valid_actions.append(card)

            # If non-yellow chip picked, can't select any card
            if not holding_area_chips.empty:
                continue

            # If no chip picked, can select any which the player can afford
            if game_state.game.current_player.can_afford(card.chip_cost):
                valid_actions.append(card)

    return valid_actions

class GameState(object):
    def __init__(self):
        self._is_turn_complete = None
        self._valid_actions = None
        self.game = None

    def update(self, game):
        self.__init__()
        self.game = game

    @property
    def is_turn_complete(self):
        if self._is_turn_complete is None:
            self._is_turn_complete = \
                get_is_turn_complete()
        return self._is_turn_complete

    @property
    def valid_actions(self):
        if self._valid_actions is None:
            self._valid_actions = get_valid_actions()
        return self._valid_actions

game_state = GameState()
