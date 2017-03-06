import pygame
from itertools import combinations

from chip_types import ChipType

from drawing_surface import draw_table
# from game_objects import IN_PLAYER_AREA, IN_HOLDING_AREA, IN_SUPPLY, IN_RESERVED_AREA
# from game_objects import Chip

class Game(object):
    """
    Container for game elements - table, players, holding area
    Plus some helper methods
    """

    def __init__(self):
        self.components = None
        self.current_player = None
        self.buttons = None
        self.players = None

    def init_game(self, players, buttons, components):
        self.players = players
        self.components = components
        self.buttons = buttons

    @property
    def valid_actions(self):
        return self.components.valid_pieces(self.current_player)

    @property
    def player_count(self):
        """
        Some of the game rules depend on the number of players
        :return: Number of players
        """
        return len(self.players)

    def next_player(self):
        """
        Move to the next player
        """
        i = self.players.index(self.current_player)

        # Current player now waiting for their next turn
        self.current_player.wait()

        # Find the index of the next player
        try:
            self.current_player = self.players[i + 1]
        except IndexError:
            self.current_player = self.players[0]

        self.current_player.start()

    def embody(self):
        """
        Embody the game
        - Create all available buttons
        - Draw the table, holding and player areas
        """

        # Remove previously created buttons
        # print("Reinstate this: in game_state")
        game.buttons.reset()

        # self._draw()
        draw_table()

        self.components.embody()
        # self.components.embody()
        # self.table.embody()
        for player in self.players:
            player.embody()
        # self.holding_area.embody()
        pygame.display.flip()

    def refresh_display(self):
        """
        Show the current game state
        Called after every state change, e.g. after player
        clicks on a piece (which moves it to the holding area)
        """
        self.embody()
        pygame.display.flip()

    def show_state(self):
        print(", ".join(["%s: %s" % (player.name, player.state) for player in self.players]))

    # @property
    # def earned_tiles(self):
    #     if self._earned_tiles is None:
    #         self._earned_tiles = self._get_earned_tiles
    #         print("Earned %s tiles" % len(self._earned_tiles))
    #     return self._earned_tiles

    @property
    def earned_multiple_tiles(self):
        return len(self.earned_tiles) > 1

    @property
    def earned_single_tile(self):
        return len(self.earned_tiles) == 1

    @property
    def earned_tiles(self):
        # TODO: Remove 'result'
    # def _get_earned_tiles(self):
        result = [tile for tile in game.table.tiles.tiles if game.current_player.can_afford(tile.chip_cost)]
        print("Earned %s tiles" % len(result))
        return result

    @property
    def is_turn_complete(self):
        holding_area = self.holding_area
        # 2 of same chip selected
        if len(holding_area.chips) == 2 \
                and holding_area.chips.different_types == 1:
            return True

        # 3 different chips selected
        if len(holding_area.chips) == 3 and holding_area.chips.different_types == 3:
            return True

        # 1 card selected
        if holding_area.card:
            return True

        table_chips = game.table.chips

        # One non-yellow chip taken, no other colours available,
        # and two or less of this colour available
        if holding_area.chips.any_non_yellow_chips \
                and len(holding_area.chips) == 1:
            held_chip = holding_area.chips.chips[0]
            if not table_chips.has_other_colours([held_chip]) \
                    and table_chips.count(held_chip.chip_type) <= 2:
                return True

        # Two chips taken, no other colours available
        if len(holding_area.chips) == 2 and \
                not table_chips.has_other_colours(holding_area.chips.chips):
            return True

        return False

    # @property
    # def valid_actions(self):


        # TODO: Either cache this, or use an "is_valid_action(item)" function
        # return []
        # holding_area_chips = self.holding_area.chips
        # table_chips = self.table.chips
        # reserved_cards = self.current_player.reserved
        #
        # result = []
        # result += holding_area_chips.chips
        # if self.holding_area.card:
        #     result.append(self.holding_area.card)
        #
        # if self.is_turn_complete:
        #     return result
        #
        # # Which chips can be selected?
        # for chip_type in ChipType:
        #     chip = table_chips.first_chip_of_type(chip_type)
        #
        #     # No chip of this type in the supply
        #     if not chip:
        #         continue
        #
        #     # Can only take yellow disk if < 3 cards reserved
        #     if chip.chip_type == ChipType.yellow_gold \
        #             and len(reserved_cards) > 2:
        #         continue
        #
        #     # If yellow selected, can't select any other chips
        #     if holding_area_chips.any_chip_of_type(ChipType.yellow_gold):
        #         continue
        #
        #     # If any (non-yellow) chip selected, can't select yellow chip
        #     if not holding_area_chips.empty \
        #             and chip_type == ChipType.yellow_gold:
        #         continue
        #
        #     # If already selected 2 chips, can't select a colour again
        #     if len(holding_area_chips) == 2 and \
        #             holding_area_chips.any_chip_of_type(chip_type):
        #         continue
        #
        #     # If already selected 1 chip, can't select that colour again if
        #     # this are 2 or less chips of that colour (not counting the one
        #     # already selected)
        #     if len(holding_area_chips) == 1 \
        #             and holding_area_chips.any_chip_of_type(chip_type) \
        #             and table_chips.count(chip_type) <= 2:
        #         continue
        #
        #     result.append(chip)
        #
        # # Which cards can be selected?
        # # TODO: More Pythonic way to loop through this?
        # for row in game.table.card_grid.cards:
        #     for card in row:
        #         if not card:
        #             continue
        #
        #         # If yellow chip picked, can select all
        #         if holding_area_chips.any_chip_of_type(
        #                 ChipType.yellow_gold
        #         ):
        #             result.append(card)
        #
        #         # If non-yellow chip picked, can't select any card
        #         if not holding_area_chips.empty:
        #             continue
        #
        #         # If no chip picked, can select any which the player can afford
        #         if game.current_player.can_afford(card.chip_cost):
        #             result.append(card)
        #
        # # Any reserved cards which this player can afford?
        # for card in game.current_player.reserved.cards:
        #     if game.current_player.can_afford(card.chip_cost):
        #         result.append(card)

        # return []
        # return result

    @property
    def valid_action_sets(self):
        """
        This player can take:
        3 different (non-yellow) chips
        2 of the same chip, if at least 4 of that type available
        Any card which they can afford
        1 yellow chip plus any card (reserve - don't take)
        """

        # result = {}
        # table_chips = game.table.chips
        # table_chips_by_type = table_chips.chips_by_type()
        #
        # # 3 different (non-yellow) chips
        # available_chips = [
        #     chip for chip in table_chips.top_chips()
        #     if chip.chip_type is not ChipType.yellow_gold]
        #
        # result['3 chips'] = list(combinations(available_chips, 3)) \
        #     if len(available_chips) >= 3 \
        #     else [available_chips]
        #
        # result['2 chips'] = [
        #     table_chips_by_type[chip_type][:2] for chip_type in table_chips_by_type.keys()
        #     if len(table_chips_by_type[chip_type]) >= 4
        #     ]
        #
        # result['card'] = []
        # result['reserve card'] = []
        # first_yellow_chip = table_chips.first_chip_of_type(
        #     ChipType.yellow_gold)
        # for row in game.table.card_grid.cards:
        #     for card in row:
        #         if not card:
        #             continue
        #
        #         # If no chip picked, can select any which the player can afford
        #         if game.current_player.can_afford(card.chip_cost):
        #             result['card'].append([card])
        #
        #         if first_yellow_chip:
        #             result['reserve card'].append(
        #                 [card, first_yellow_chip]
        #             )
        #
        # result['buy reserved'] = []
        # for card in game.current_player.reserved.cards:
        #     if game.current_player.can_afford(card.chip_cost):
        #         result['buy reserved'].append(card)

        return result

game = Game()
