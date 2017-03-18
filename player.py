from transitions import Machine

from chip_types import ChipType
from game import game
from states import PlayerStates
from embody import EmbodyPlayerMixin
from game_components import Card


class Player(EmbodyPlayerMixin):
    states = [
        PlayerStates.player_waiting,
        PlayerStates.turn_started,
        PlayerStates.turn_in_progress,
        PlayerStates.turn_valid,
        PlayerStates.tiles_offered,
        PlayerStates.tile_selected,
        PlayerStates.too_many_chips,
        PlayerStates.turn_finished,
    ]

    transitions = [
        # Start a player's turn
        dict(trigger='start', source=PlayerStates.player_waiting, dest=PlayerStates.turn_started, after=['show_state'],
             conditions='human_player'),

        # For AI players, select the move and take the (first) component
        dict(trigger='start', source=PlayerStates.player_waiting, dest=PlayerStates.turn_started,
             after=['ai_makes_move', 'show_state'],
             conditions='ai_player'),

        # For AI players, if multiple tiles offered, AI should select on and then wait for confirmation
        dict(trigger='confirm', source=PlayerStates.turn_started, dest=PlayerStates.tile_selected,
             conditions=['ai_player', 'earned_multiple_tiles'],
             before='_confirm_component_selection', after=['ai_selects_tile', 'show_state']),

        # For human players, give player a chance to select a tile
        dict(trigger='confirm', source=PlayerStates.turn_started, dest=PlayerStates.tiles_offered,
             conditions=['human_player', 'earned_multiple_tiles'],
             before='_confirm_component_selection', after='show_state'),

        # For AI and human players, if one tile available, show and and wait for confirmation
        dict(trigger='confirm', source=PlayerStates.turn_started, dest=PlayerStates.tile_selected,
             conditions='earned_single_tile',
             before='_confirm_component_selection', after=['player_selects_single_tile', 'show_state']),

        # If no tile available, but taken too many chips, put some back first
        # TODO: Automate this for the AI
        dict(trigger='confirm', source=PlayerStates.turn_started,
             dest=PlayerStates.turn_finished,
             conditions=['earned_no_tiles', 'too_many_chips'],
             before='_confirm_component_selection', after='show_state'),

        # If no tile available, and not too many chips taken, go straight to the end of the turn
        dict(trigger='confirm', source=PlayerStates.turn_started, dest=PlayerStates.turn_finished,
             conditions=['earned_no_tiles', 'not_too_many_chips'],
             before='_confirm_component_selection', after='show_state'),

        # Confirm selected tile, if too many chips taken, put some back first
        dict(trigger='confirm', source=PlayerStates.tiles_offered, dest=PlayerStates.turn_finished,
             conditions=['too_many_chips'],
             before='_confirm_component_selection',
             after='show_state'),

        # Confirm selected tile, if not too many chips taken, end of turn
        dict(trigger='confirm', source=PlayerStates.tiles_offered, dest=PlayerStates.turn_finished,
             unless=['too_many_chips'],
             before='_confirm_component_selection',
             after='show_state'),

        # Confirm selected chips to return, end of turn
        dict(trigger='confirm', source=PlayerStates.too_many_chips, dest=PlayerStates.turn_finished,
             before='_confirm_component_selection',
             after='show_state'),

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

    def ai_selects_tile(self):
        self.AI.select_tile()

    def player_selects_single_tile(self):
        game.mechanics.player_selects_single_tile()

    def on_enter_turn_started(self):
        game.embody()

    def on_enter_turn_finished(self):
        game.mechanics.next_player()

    def cancel_move_in_progress(self):
        for component in game.components.holding_area_components:
            component.move_back()

    def show_state(self):
        game.mechanics.show_state()

    def human_player(self):
        return game.current_player.is_human

    def ai_player(self):
        return not game.current_player.is_human

    @property
    def is_human(self):
        return self.AI is None

    @property
    def is_current_player(self):
        return self.state != PlayerStates.player_waiting

    def complete_turn_taken(self):
        """
        Has this player taken a complete set of items?
        - 3 different chips
        - 2 similar chips
        - 1 card
        :return:
        """
        return game.mechanics.is_turn_complete

    def empty_selection(self):
        """
        Has this player no items yet?
        :return:
        """
        return game.components.holding_area_components.is_empty

    def earned_multiple_tiles(self):
        """
        Are there multiple noble tiles available for this player?
        :return:
        """
        return game.mechanics.earned_multiple_tiles

    def earned_single_tile(self):
        """
        Is there a single noble tile available for this player?
        :return:
        """
        return game.mechanics.earned_single_tile

    def earned_no_tiles(self):
        return not game.mechanics.earned_multiple_tiles and not game.mechanics.earned_single_tile

    def end_of_game(self):
        return game.last_player and game.mechanics.final_round

    @property
    def components(self):
        return game.components.filter(player=self)

    @property
    def points(self):
        return game.mechanics.points_for_player(self)

    def chip_count(self):
        return len(game.components.chips_for_player(self))

    def too_many_chips(self):
        return self.chip_count() > 10

    def not_too_many_chips(self):
        return not self.too_many_chips()

    def _confirm_component_selection(self):
        holding_area_components = game.components.holding_area_components
        reserved = (game.components.holding_area_chips.count_for_colour(ChipType.yellow_gold) > 0)

        for c in holding_area_components:
            c.player = game.current_player
            if isinstance(c, Card):
                if reserved:
                    c.to_reserved_area()
                    continue
                game.mechanics.pay_chip_cost(c.chip_cost, self)
            c.to_player_area()
        game.mechanics.draw_cards()

    # def _confirm_tile_selection(self):
    #     for tile in list(game.components.holding_area_components)[:]:
    #         tile.to_player_area()
    #         tile.player = game.current_player
    #
    def _cancel_tile_selection(self):
        for tile in list(game.components.holding_area_components)[:]:
            tile.to_supply()
