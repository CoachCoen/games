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

    @property
    def components(self):
        return game.components.filter(player=self)

    @property
    def points(self):
        return self.cards.points + self.tiles.points

    def _confirm_component_selection(self):
        holding_area_components = game.components.holding_area_components
        reserved = (holding_area_components.count_for_colour(ChipType.yellow_gold) > 0)

        for c in holding_area_components:
            c.player = game.current_player
            if isinstance(c, Card):
                if reserved:
                    c.to_reserved_area()
                    continue
                game.mechanics.pay_chip_cost(c.chip_cost, self)
            c.to_player_area()
        game.mechanics.draw_cards()
