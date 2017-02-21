from itertools import combinations

from data import ChipType
from game_game import game


class GameState(object):
    def __init__(self):
        self._is_turn_complete = None
        self._valid_actions = None
        self._valid_action_sets = None

    def update(self):
        self.__init__()

    @property
    def is_turn_complete(self):
        if self._is_turn_complete is None:
            self._is_turn_complete = \
                self._get_is_turn_complete()
        return self._is_turn_complete

    @property
    def valid_actions(self):
        if self._valid_actions is None:
            self._valid_actions = self._get_valid_actions()
        return self._valid_actions

    @property
    def valid_action_sets(self):
        if self._valid_action_sets is None:
            self._valid_action_sets = self._get_valid_action_sets()
        return self._valid_action_sets

    @staticmethod
    def _get_is_turn_complete():
        holding_area = game.holding_area
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
                and not game.table.chips.any_non_yellow_chips:
            return True

        return False

    def _get_valid_actions(self):
        if self.is_turn_complete:
            return []

        holding_area_chips = game.holding_area.chips
        table_chips = game.table.chips

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
                game.table.chips.first_chip_of_type(chip_type)
            )

        # Which cards can be selected?
        # TODO: More Pythonic way to loop through this?
        for row in game.table.card_grid:
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
                if game.current_player.can_afford(card.chip_cost):
                    valid_actions.append(card)

        return valid_actions

    @staticmethod
    def _get_valid_action_sets():
        """
        This player can take:
        3 different (non-yellow) chips
        2 of the same chip, if at least 4 of that type available
        Any card which they can afford
        1 yellow chip plus any card (reserve - don't take)
        """

        valid_action_sets = {}
        table_chips = game.table.chips

        # 3 different (non-yellow) chips
        available_chips = [
            chip for chip in table_chips.top_chips()
            if chip.chip_type is not ChipType.yellow_gold]

        valid_action_sets['3 chips'] = list(combinations(available_chips, 3)) \
            if len(available_chips) >= 3 \
            else []

        valid_action_sets['2 chips'] = table_chips.top_two_chips_by_type()

        valid_action_sets['card'] = []
        valid_action_sets['reserve card'] = []
        first_yellow_chip = table_chips.first_chip_of_type(
            ChipType.yellow_gold)
        for row in game.table.card_grid:
            for card_slot in row:
                card = card_slot.card
                if not card:
                    continue

                # If no chip picked, can select any which the player can afford
                if game.current_player.can_afford(card.chip_cost):
                    valid_action_sets['card'].append([card])

                if first_yellow_chip:
                    valid_action_sets['reserve card'].append(
                        [card, first_yellow_chip]
                    )

        return valid_action_sets
