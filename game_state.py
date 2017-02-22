import pygame
from itertools import combinations

from chip_types import ChipType
# from data import ChipType


class Game(object):
    """
    Container for game elements - table, players, holding area
    Plus some helper methods
    """

    def __init__(self):
        self.players = None
        self.table = None
        self.holding_area = None
        self.buttons = None
        # self.chip_types = None
        self._is_turn_complete = None
        self._valid_actions = None
        self._valid_action_sets = None

    def init_game(self, players, table, holding_area, buttons):
        self.players = players
        self.table = table
        self.holding_area = holding_area
        self.buttons = buttons
        # self.chip_types = chip_types


    @property
    def player_count(self):
        """
        Some of the game rules depend on the number of players
        :return: Number of players
        """
        return len(self.players)

    @property
    def current_player(self):
        """
        Players can be in different states. All but one player
        will always be 'waiting', whilst the other (current) player
        will be in one of the other states
        :return: The one player who currently isn't 'waiting'
        """
        return [p for p in self.players if p.is_current_player][0]

    def next_player(self):
        """
        Move to the next player
        """
        current = self.current_player

        # Confirm the current player's action
        current.confirm()

        # Find the index of the next player
        i = self.players.index(current)
        try:
            next_p = self.players[i + 1]
        except IndexError:
            next_p = self.players[0]

        # The next player can start their turn
        next_p.start()

    def embody(self):
        """
        Embody the game
        - Create all available buttons
        - Draw the table, holding and player areas
        """

        # Remove previously created buttons
        game.buttons.reset()

        self.table.embody()
        for player in self.players:
            player.embody()
        self.holding_area.embody()

    def refresh_display(self):
        """
        Show the current game state
        Called after every state change, e.g. after player
        clicks on a piece (which moves it to the holding area)
        """
        self.embody()
        pygame.display.flip()

    def refresh_state(self):
        self._is_turn_complete = None
        self._valid_actions = None
        self._valid_action_sets = None

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

    def _get_is_turn_complete(self):
        holding_area = self.holding_area
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

        holding_area_chips = self.holding_area.chips
        table_chips = self.table.chips

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

            valid_actions.append(chip)

        # Which cards can be selected?
        # TODO: More Pythonic way to loop through this?
        for row in game.table.card_grid.cards:
            for card_slot in row:
                card = card_slot.card
                if not card:
                    continue

                # If yellow chip picked, can select all
                if holding_area_chips.any_chip_of_type(
                        ChipType.yellow_gold
                ):
                    valid_actions.append(card)

                # If non-yellow chip picked, can't select any card
                if not holding_area_chips.empty:
                    continue

                # If no chip picked, can select any which the player can afford
                if game.current_player.can_afford(card.chip_cost):
                    valid_actions.append(card)

        return valid_actions

    def _get_valid_action_sets(self):
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
        for row in game.table.card_grid.cards:
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


game = Game()
