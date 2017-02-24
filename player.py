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


class Player(object):
    # TODO: Refactor this? Replace with enum? Move comments to top?
    states = [
        WAITING,     # someone else's turn
        STARTED,     # turn started, nothing taken yet
        IN_PROGRESS,     # turn started, something taken
        VALID,           # taken complete set of items, now confirm
        TILES_OFFERED,       # one or more noble tiles can be taken
        TILE_SELECTED        # noble tile selected, now confirm
    ]

    transitions = [
        # Start a player's turn
        dict(trigger='start', source=WAITING, dest=STARTED),

        # Take a component, if complete turn taken go to VALID, otherwise
        # go to/stay in IN PROGRESS
        dict(trigger='take_component', source=[STARTED, IN_PROGRESS],
             dest=IN_PROGRESS, unless='complete_turn_taken', after='refresh_game_state'),
        dict(trigger='take_component', source=[STARTED, IN_PROGRESS],
             dest=VALID, conditions='complete_turn_taken', after='refresh_game_state'),

        # Return a component, if empty selection go to STARTED, otherwise
        # stay in IN PROGRESS
        dict(trigger='return_component', source=IN_PROGRESS, dest=STARTED,
             conditions='empty_selection', after='refresh_game_state'),
        dict(trigger='return_component', source=IN_PROGRESS, dest=IN_PROGRESS,
             unless='empty_selection', after='refresh_game_state'),

        # Valid (set of components) selected - confirm/reject?
        # TODO: Re-instate once tiles, etc, in place
        # dict(trigger='confirm', source=VALID, dest=TILES_OFFERED,
        #      conditions='earned_multiple_tiles'),
        # dict(trigger='confirm', source=VALID, dest=TILE_SELECTED,
        #      conditions='earned_single_tile'),
        # dict(trigger='confirm', source=VALID, dest=WAITING,
        #      unless=['earned_multiple_tiles', 'earned_single_tile']),
        dict(trigger='confirm', source=[IN_PROGRESS], dest=WAITING),

        dict(trigger='cancel', source=[IN_PROGRESS, VALID], dest=STARTED),

        # Multiple nobles tiles offered, take one
        dict(trigger='select_tile', source=[TILES_OFFERED, TILE_SELECTED],
             dest=TILE_SELECTED),

        # Confirm selection, end of turn
        dict(trigger='take_tile', source=TILE_SELECTED, dest=WAITING)
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

    def on_enter_turn_started(self):
        if self.AI:
            self.AI.take_turn()

    @staticmethod
    def refresh_game_state():
        game.refresh_state()

    def has_chips_of_type(self, chip_type):
        # TODO: Refactor: better way to find the right chip stack
        for chip_stack in self.chip_stacks.chip_stacks:
            if chip_stack.chip.chip_type == chip_type:
                return chip_stack.chip_count
        return 0

    # def pay_cost_for_single_chip_type(self, chip_type, cost):
    #     # TODO: Refactor, create index?
    #     for chip_stack in self.chip_stacks.chip_stacks:
    #         if chip_stack.chip.chip_type == chip_type:
    #             available = chip_stack.chip_count
    #
    #             # Return the chips
    #             # TODO: Better way of doing this?
    #             for _ in range(min(available, cost)):
    #                 chip_stack.chip.source.add_one()
    #
    #             if available >= cost:
    #                 chip_stack.chip_count -= cost
    #                 return 0
    #             else:
    #                 chip_stack.chip_count = 0
    #                 return cost - available
    #     # Should never get here

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

        # chips_shortage = 0
        # for chip_type in [chip_type for chip_type in ChipType if chip_type is not ChipType.yellow_gold]:
        #     count = chip_cost.count(chip_type)
        #
        #     available = self.chips.count(chip_type) + self.cards.produces_for_chip_type(chip_type)
        #
        #
        #
        # chips_shortage = 0
        # for chip in chip_cost.chips:
        #     if not self.chips.pay_chip_of_type(chip.chip_type):
        #         chips_shortage += 1
        #
        # for _ in range(chips_shortage):
        #     self.chips.pay_chip_of_type(ChipType.yellow_gold)

        # for chip_stack in chip_cost.chip_stacks:
        #     count = chip_stack.chip_count
        #     if not count:
        #         continue
        #
        #     chips_shortage += self.pay_cost_for_single_chip_type(
        #         chip_stack.chip.chip_type, count
        #     )
        #
        # if chips_shortage:
        #     self.pay_cost_for_single_chip_type(
        #         ChipType.yellow_gold, chips_shortage
        #     )

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

    def add_chip(self, chip):
        # TODO: Refactor - maybe method for ChipStack?
        for chip_stack in self.chip_stacks.chip_stacks:
            if chip_stack.chip.chip_type == chip.chip_type:
                chip_stack.chip_count += 1

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
        return False

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
        pass

    def earned_single_tile(self):
        """
        Is there a single noble tile available for this player?
        :return:
        """
        pass

    def start_turn(self):
        """
        Do this before going into the 'turn started' stage
        :return:
        """
        pass

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

        # for i, chip_type in enumerate(ChipType):
        #     total = self.cards.count_for_reward_type(chip_type)
        #     chip_stack = self.chip_stacks.get_stack_for_chip_type(chip_type)
        #
        #     if total:
        #         location = (
        #             config.player_chip_stack_location.x +
        #             i * (config.chip_size + config.chip_spacing) -
        #             0.5 * config.chip_size,
        #             config.player_chip_stack_location.y + config.chip_size,
        #             config.chip_size, config.chip_size
        #         )
        #         draw_rectangle(
        #             location,
        #             colour=chip_stack.chip.colour,
        #             player_order=self.player_order)
        #         draw_text(
        #             location,
        #             str(total),
        #             player_order=self.player_order,
        #             text_colour=chip_stack.chip.colour,
        #             font_size=config.chip_cost_scaling * config.chip_font_size,
        #             reverse_colour=True
        #         )
        #
        #     # TODO: Move chip_stack.embody into self.embody()
        #     if chip_stack.chip_count:
        #         chip_stack.embody(
        #             config.player_chip_stack_location +
        #             Vector(i * (config.chip_size + config.chip_spacing), 0),
        #             scaling_factor=config.chip_cost_scaling,
        #             player_order=self.player_order
        #         )
        #         total += chip_stack.chip_count
        #
        #     if total:
        #         location = (config.player_chip_stack_location.x +
        #                     i * (config.chip_size + config.chip_spacing) -
        #                     0.5 * config.chip_size,
        #                     config.player_chip_stack_location.y +
        #                     2.5 * config.chip_size,
        #                     config.chip_size, config.chip_size)
        #
        #         draw_text(
        #             location,
        #             str(total),
        #             player_order=self.player_order,
        #             text_colour=chip_stack.chip.colour
        #         )
