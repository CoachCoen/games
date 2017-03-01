from transitions import Machine

from game_objects import ComponentCollectionFactory, ChipCollection
from drawing_surface import draw_rectangle, draw_text, draw_squares_row, \
    draw_circles_row
from drawing_surface import ColourPalette
from settings import config
from game_objects import ChipType
from game_state import game

WAITING = 'waiting_for_turn'
STARTED = 'turn_started'
IN_PROGRESS = 'turn_in_progress'
VALID = 'valid_turn'
TILES_OFFERED = 'tiles_on_offer'
TILE_SELECTED = 'tile_selected'
TURN_FINISHED = 'turn_finished'


class Player(object):
    # TODO: Refactor this? Replace with enum? Move comments to top?
    states = [
        WAITING,     # someone else's turn
        STARTED,     # turn started, nothing taken yet
        IN_PROGRESS,     # turn started, something taken
        VALID,           # taken complete set of items, now confirm
        TILES_OFFERED,       # one or more noble tiles can be taken
        TILE_SELECTED,        # noble tile selected, now confirm
        TURN_FINISHED,      # End of turn
    ]

    transitions = [
        # Start a player's turn
        dict(trigger='start', source=WAITING, dest=STARTED, after=['show_state'],
             conditions='human_player'),

        dict(trigger='start', source=WAITING, dest=VALID, after=['ai_makes_move', 'show_state'],
             conditions='ai_player'),

        # Take a component, if complete turn taken go to VALID, otherwise
        # go to/stay in IN PROGRESS
        dict(trigger='take_component', source=[STARTED, IN_PROGRESS],
             dest=IN_PROGRESS, unless='complete_turn_taken', after='show_state'),
        dict(trigger='take_component', source=[STARTED, IN_PROGRESS],
             dest=VALID, conditions='complete_turn_taken', after='show_state'),

        # Return a component, if empty selection go to STARTED, otherwise
        # stay in IN PROGRESS
        dict(trigger='return_component', source=IN_PROGRESS, dest=STARTED,
             conditions='empty_selection', after='show_state'),
        dict(trigger='return_component', source=IN_PROGRESS, dest=IN_PROGRESS,
             unless='empty_selection', after='show_state'),

        # Valid (set of components) selected - confirm/reject?
        dict(trigger='confirm', source=VALID, dest=TILES_OFFERED,
             conditions='earned_multiple_tiles', after='show_state'),
        dict(trigger='confirm', source=VALID, dest=TILE_SELECTED,
             conditions='earned_single_tile', after='show_state'),
        dict(trigger='confirm', source=VALID, dest=TURN_FINISHED,
             unless=['earned_multiple_tiles', 'earned_single_tile'],
             before='_confirm_component_selection', after='show_state'),

        dict(trigger='cancel', source=[IN_PROGRESS, VALID], dest=STARTED, after='show_state'),

        # Multiple nobles tiles offered, take one
        dict(trigger='select_tile', source=[TILES_OFFERED, TILE_SELECTED],
             dest=TILE_SELECTED, after='show_state'),

        # Confirm selection, end of turn
        dict(trigger='take_tile', source=TILE_SELECTED, dest=TURN_FINISHED, after='show_state'),

        # Back to waiting
        dict(trigger='wait', source=TURN_FINISHED, dest=WAITING, after='show_state'),
    ]

    def __init__(self, name, AI, player_order):
        self.name = name
        self.player_order = player_order
        self.AI = AI
        if AI:
            self.AI.player = self

        component_collection_factory = ComponentCollectionFactory()
        self.cards = component_collection_factory('card', '')
        self.chips = ChipCollection()
        self.tiles = component_collection_factory('tile', '')
        self.reserved = component_collection_factory('card', '')
        self.machine = Machine(
            model=self,
            states=Player.states,
            transitions=Player.transitions,
            initial=WAITING
        )

    def ai_makes_move(self):
        self.AI.take_turn()

    def on_enter_turn_started(self):
        game.refresh_display()

    def on_enter_turn_finished(self):
        game.next_player()

    def show_state(self):
        # game.show_state()
        pass
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
        return self.state != WAITING

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
        return game.holding_area.is_empty

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

    def embody(self):
        self._draw()

        chip_counts = self.chips.counts_for_type
        card_counts = self.cards.counts_for_type
        draw_circles_row(
            config.player_chip_stack_location,
            chip_counts,
            player_order=self.player_order
        )
        draw_squares_row(
            config.player_card_deck_location,
            card_counts,
            player_order=self.player_order
        )
        self.reserved.embody(config.player_reserved_location,
                             player_order=self.player_order)

    # TODO: Refactor this - messy?
    def _draw(self):
        draw_rectangle(
            (0, 0, config.player_area_size.x, config.player_area_size.y),
            player_order=self.player_order,
            colour=ColourPalette.active_player_area
            if self.state != WAITING
            else ColourPalette.player_area
        )
        draw_text(
            (config.player_name_location.x, config.player_name_location.y),
            self.name,
            player_order=self.player_order
        )
        if self.points:
            draw_text(
                (config.player_points_location.x,
                 config.player_points_location.y),
                str(self.points),
                player_order=self.player_order
            )

    def _confirm_component_selection(self):
        held_card = game.holding_area.card

        if game.holding_area.chips.any_chip_of_type(ChipType.yellow_gold):
            # Yellow chip taken, so reserved card
            self.reserve_card(held_card)
            game.table.card_grid.fill_empty_spaces()

        elif held_card:
            # Take card
            self.pay_cost(held_card.chip_cost)

            # Draw a new card and assign it to the original card's slot
            self.add_card(held_card)
            game.table.card_grid.fill_empty_spaces()

        game.holding_area.card = None
        game.holding_area.chips.transfer_chips(self.chips)
