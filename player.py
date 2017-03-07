from transitions import Machine

from drawing_surface import draw_rectangle
from drawing_surface import ColourPalette
from settings import config
from chip_types import ChipType
from game_state import game
from states import PlayerStates
from embody import EmbodyPlayerMixin
from game_objects import Card


class Player(EmbodyPlayerMixin):
    states = [
        PlayerStates.player_waiting,
        PlayerStates.turn_started,
        PlayerStates.turn_in_progress,
        PlayerStates.turn_valid,
        PlayerStates.tiles_offered,
        PlayerStates.tile_selected,
        PlayerStates.turn_finished,
    ]

    transitions = [
        # Start a player's turn
        dict(trigger='start', source=PlayerStates.player_waiting, dest=PlayerStates.turn_started, after=['show_state'],
             conditions='human_player'),

        # For AI players, select the move and take the (first) component
        dict(trigger='start', source=PlayerStates.player_waiting, dest=PlayerStates.turn_valid,
             after=['ai_makes_move', 'show_state'],
             conditions='ai_player'),

        # Take a component, if complete turn taken go to VALID, otherwise
        # go to/stay in IN PROGRESS

        dict(trigger='take_component', source=[PlayerStates.turn_started, PlayerStates.turn_in_progress],
             dest=PlayerStates.turn_in_progress, unless='complete_turn_taken', after='show_state'),
        dict(trigger='take_component', source=[PlayerStates.turn_started, PlayerStates.turn_in_progress],
             dest=PlayerStates.turn_valid, conditions='complete_turn_taken', after='show_state'),

        # Return a component, if empty selection go to STARTED, otherwise
        # stay in IN PROGRESS
        dict(trigger='return_component', source=[PlayerStates.turn_in_progress, PlayerStates.turn_valid], dest=PlayerStates.turn_started,
             conditions='empty_selection', after='show_state'),
        dict(trigger='return_component', source=[PlayerStates.turn_in_progress, PlayerStates.turn_valid], dest=PlayerStates.turn_in_progress,
             unless='empty_selection', after='show_state'),

        # Valid (set of components) selected - confirm/reject?
        dict(trigger='confirm', source=PlayerStates.turn_valid, dest=PlayerStates.tiles_offered,
             conditions='earned_multiple_tiles', after='show_state'),
        dict(trigger='confirm', source=PlayerStates.turn_valid, dest=PlayerStates.tile_selected,
             conditions='earned_single_tile', after='show_state'),
        dict(trigger='confirm', source=PlayerStates.turn_valid, dest=PlayerStates.turn_finished,
             unless=['earned_multiple_tiles', 'earned_single_tile'],
             before='_confirm_component_selection', after='show_state'),

        dict(trigger='cancel', source=[PlayerStates.turn_in_progress, PlayerStates.turn_valid], dest=PlayerStates.turn_started,
             after=['cancel_move_in_progress', 'show_state']),

        # Multiple nobles tiles offered, take one
        dict(trigger='select_tile', source=[PlayerStates.tiles_offered, PlayerStates.tile_selected],
             dest=PlayerStates.tile_selected, after='show_state'),

        # Confirm selection, end of turn
        dict(trigger='take_tile', source=PlayerStates.tile_selected, dest=PlayerStates.turn_finished, after='show_state'),

        # Back to waiting
        dict(trigger='wait', source=PlayerStates.turn_finished, dest=PlayerStates.player_waiting, after='show_state'),
    ]

    def __init__(self, name, AI, player_order):
        self.name = name
        self.player_order = player_order
        self.AI = AI
        if AI:
            self.AI.player = self

        self.machine = Machine(
            model=self,
            states=Player.states,
            transitions=Player.transitions,
            initial=PlayerStates.player_waiting
        )

    def ai_makes_move(self):
        self.AI.take_turn()

    def on_enter_turn_started(self):
        game.refresh_display()

    def on_enter_turn_finished(self):
        game.next_player()

    def cancel_move_in_progress(self):
        for component in game.components.holding_area_components:
            component.move_back()
        # game.holding_area.chips.return_chips()
        #
        # if game.holding_area.card:
        #     game.table.card_grid.return_card(game.holding_area.card)
        #     game.holding_area.card = None

    def show_state(self):
        game.show_state()
        # pass
        # TODO: Remove game.show_state() method

    def human_player(self):
        return game.current_player.is_human

    def ai_player(self):
        return not game.current_player.is_human

    @property
    def is_human(self):
        return self.AI is None

    def has_chips_of_type(self, chip_type):
        # TODO: Refactor: better way to find the right chip stack
        for chip_stack in self.chip_stacks.chip_stacks:
            if chip_stack.chip.chip_type == chip_type:
                return chip_stack.chip_count
        return 0

    def pay_cost(self, chip_cost):
        """
        Pay the chip_cost, after deduction any discounts through cards this players owns
        """
        # Assumption: Can afford it
        cost_by_type = chip_cost.counts_for_type

        for chip_type in ChipType:
            to_pay = cost_by_type[chip_type] - self.cards.produces_for_chip_type(chip_type)

            if to_pay:
                for _ in range(to_pay):
                    # pay the chip - or pay a gold one if normal chip not available
                    if not self.chips.pay_chip_of_type(chip_type):
                        self.chips.pay_chip_of_type(ChipType.yellow_gold)

    @property
    def is_current_player(self):
        return self.state != PlayerStates.player_waiting

    def can_afford(self, chip_cost):
        chips_shortage = 0
        for chip_type in [chip_type for chip_type in ChipType if chip_type is not ChipType.yellow_gold]:
            count = chip_cost.count(chip_type)

            available = self.chips.count(chip_type) + self.cards.produces_for_chip_type(chip_type)
            if available < count:
                chips_shortage += \
                    count - available

        # Missing chips can be replaced by yellow chips
        return chips_shortage <= self.chips.count(ChipType.yellow_gold)

    def add_card(self, card):
        self.cards.add(card)

    def reserve_card(self, card):
        self.reserved.add(card)

    def complete_turn_taken(self):
        """
        Has this player taken a complete set of items?
        - 3 different chips
        - 2 similar chips
        - 1 card
        :return:
        """
        return game.is_turn_complete

    def empty_selection(self):
        """
        Has this player no items yet?
        :return:
        """
        return game.components.holding_area_components.is_empty
        # return game.holding_area.is_empty

    def earned_multiple_tiles(self):
        """
        Are there multiple noble tiles available for this player?
        :return:
        """
        return game.earned_multiple_tiles

    def earned_single_tile(self):
        """
        Is there a single noble tile available for this player?
        :return:
        """
        return game.earned_single_tile

    @property
    def points(self):
        return self.cards.points + self.tiles.points

    def _confirm_component_selection(self):
        for c in game.components.holding_area_components:
            if isinstance(c, Card):
                game.components.pay_chip_cost(c.chip_cost, self)
            c.to_player_area()
            c.player = game.current_player
        game.components.draw_cards()

        # for chip in game.components.holding_area_chips:
        #     chip.player = game.current_player
        #     chip.to_player_area()
        # held_card = game.holding_area.card
        #
        # if game.holding_area.chips.any_chip_of_type(ChipType.yellow_gold):
        #     # Yellow chip taken, so reserved card
        #     self.reserve_card(held_card)
        #     game.table.card_grid.fill_empty_spaces()
        #
        # elif held_card:
        #     # Take card
        #     self.pay_cost(held_card.chip_cost)
        #
        #     # Draw a new card and assign it to the original card's slot
        #     self.add_card(held_card)
        #     game.table.card_grid.fill_empty_spaces()
        #
        # game.holding_area.card = None
        # game.holding_area.chips.transfer_chips(self.chips)
