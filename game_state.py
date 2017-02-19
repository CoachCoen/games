from data import ChipType

def get_is_turn_complete():
    holding_area = game_state.game.holding_area
    # 2 of same chip selected
    if len(holding_area.chips) == 2:
        if len({c.chip_type for c in holding_area.chips}) == 1:
            return True

    # 3 different chips selected
    if len(holding_area.chips) == 3:
        return True

    # 1 card selected
    if holding_area.card:
        return True

    # No chips left to take
    # TODO: Fix/Test this
    # if holding_area.chips and game_state.game.table.chip_stacks.empty:
    #     return True

    return False

def get_valid_actions():
    if game_state.is_turn_complete:
        return []

    selected_chips = game_state.game.holding_area.chips

    valid_actions = []

    # Which chips can be selected?
    for chip_stack in game_state.game.table.chip_stacks.chip_stacks:
        # If yellow selected, can't select any other chips
        if selected_chips \
                and selected_chips[0].chip_type == ChipType.yellow_gold:
            continue

        # If any (non-yellow) chip selected, can't select yellow chip
        if selected_chips \
                and chip_stack.chip.chip_type == ChipType.yellow_gold:
            continue

        # If already selected 2 chips, can't select a colour again
        if len(selected_chips) == 2 and \
                any(c.chip_type == chip_stack.chip.chip_type
                    for c in selected_chips):
            continue

        # If already selected 1 chip, can't select that colour again if
        # this are 3 or less chips of that colour
        if len(selected_chips) == 1 \
                and chip_stack.chip.chip_type == selected_chips[0].chip_type \
                and chip_stack.chip_count <= 3:
            continue

        valid_actions.append(chip_stack)

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
