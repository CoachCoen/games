from transitions import Machine

from game_objects import ComponentCollectionFactory
from drawing_surface import draw_rectangle, draw_text
from drawing_surface import ColourPalette
from settings import config, Vector
from data import ChipType
from holding_area import holding_area

WAITING = 'waiting for turn'
STARTED = 'turn started'
IN_PROGRESS = 'turn in progress'
VALID = 'valid turn'
TILES_OFFERED = 'tiles on offer'
TILE_SELECTED = 'tile selected'


# class PlayerState(object):
#     def __init__(self, name):
#         self.name = name
#
#



class Player(object):
    # TODO: Refactor this? Replace with enum? Move comments to top?
    states = [
        WAITING,     # someone else's turn
        STARTED,         # turn started, nothing taken yet
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
             dest=IN_PROGRESS, unless='complete_turn_taken'),
        dict(trigger='take_component', source=[STARTED, IN_PROGRESS],
             dest=VALID, conditions='complete_turn_taken'),

        # Return a component, if empty selection go to STARTED, otherwise
        # stay in IN PROGRESS
        dict(trigger='return_component', source=IN_PROGRESS, dest=STARTED,
             conditions='empty_selection'),
        dict(trigger='return_component', source=IN_PROGRESS, dest=IN_PROGRESS,
             unless='empty_selection'),

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

    def __init__(self, name, player_order):
        self.name = name
        self.player_order = player_order

        component_collection_factory = ComponentCollectionFactory()
        # self.cards = component_collection_factory('card', row_1)
        self.cards = component_collection_factory('card', '')
        # TODO: Remove this when done testing showing the players' hands
        # self.chip_stacks = component_collection_factory(
        #     'chip', '2 blue,2 white,2 black,2 green,2 red,1 yellow'
        # )
        self.chip_stacks = component_collection_factory(
            'chip', '0 blue,0 white,0 black,0 green,0 red,0 yellow'
        )
        self.tiles = component_collection_factory('tile', '')
        self.machine = Machine(
            model=self,
            states=Player.states,
            transitions=Player.transitions,
            initial=WAITING
        )

    def has_chips_of_type(self, chip_type):
        # TODO: Refactor: better way to find the right chip stack
        for chip_stack in self.chip_stacks.chip_stacks:
            if chip_stack.chip.chip_type == chip_type:
                return chip_stack.chip_count
        return 0

    def pay_cost_for_single_chip_type(self, chip_type, cost):
        # TODO: Refactor, create index?
        for chip_stack in self.chip_stacks.chip_stacks:
            if chip_stack.chip.chip_type == chip_type:
                available = chip_stack.chip_count

                # Return the chips
                # TODO: Better way of doing this?
                for _ in range(min(available, cost)):
                    chip_stack.chip.source.add_one()

                if available >= cost:
                    chip_stack.chip_count -= cost
                    return 0
                else:
                    chip_stack.chip_count = 0
                    return cost - available
        # Should never get here

    def pay_cost(self, chip_cost):
        # Assumption: Can afford it
        chips_shortage = 0
        for chip_stack in chip_cost.chip_stacks:
            count = chip_stack.chip_count
            if not count:
                continue

            chips_shortage += self.pay_cost_for_single_chip_type(
                chip_stack.chip.chip_type, count
            )

        if chips_shortage:
            self.pay_cost_for_single_chip_type(
                ChipType.yellow_gold, chips_shortage
            )

    def can_afford(self, chip_cost):
        chips_shortage = 0
        for chip_stack in chip_cost.chip_stacks:
            count = chip_stack.chip_count
            if not count:
                continue

            if self.has_chips_of_type(chip_stack.chip.chip_type) < count:
                chips_shortage += \
                    count - self.has_chips_of_type(chip_stack.chip.chip_type)

        # Missing chips can be replaced by yellow chips
        return chips_shortage <= self.has_chips_of_type(ChipType.yellow_gold)

    def add_chip(self, chip):
        # TODO: Refactor - maybe method for ChipStack?
        for chip_stack in self.chip_stacks.chip_stacks:
            if chip_stack.chip.chip_type == chip.chip_type:
                chip_stack.chip_count += 1

    def add_card(self, card):
        self.cards.add(card)

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
        return holding_area.is_empty

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

    # TODO: Refactor this - messy?
    def _draw(self):
        draw_rectangle(
            (0, 0, config.player_area_size.x, config.player_area_size.y),
            player_order=self.player_order,
            colour=ColourPalette.active_player_area
            if self.state != 'waiting for turn'
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

        for i, chip_type in enumerate(ChipType):
            total = self.cards.count_for_reward_type(chip_type)
            chip_stack = self.chip_stacks.get_stack_for_chip_type(chip_type)

            if total:
                location = (
                    config.player_chip_stack_location.x +
                    i * (config.chip_size + config.chip_spacing) -
                    0.5 * config.chip_size,
                    config.player_chip_stack_location.y + config.chip_size,
                    config.chip_size, config.chip_size
                )
                draw_rectangle(
                    location,
                    colour=chip_stack.chip.colour,
                    player_order=self.player_order)
                draw_text(
                    location,
                    str(total),
                    player_order=self.player_order,
                    text_colour=chip_stack.chip.colour,
                    font_size=config.chip_cost_scaling * config.chip_font_size,
                    reverse_colour=True
                )

            # TODO: Move chip_stack.embody into self.embody()
            if chip_stack.chip_count:
                chip_stack.embody(
                    config.player_chip_stack_location +
                    Vector(i * (config.chip_size + config.chip_spacing), 0),
                    scaling_factor=config.chip_cost_scaling,
                    player_order=self.player_order
                )
                total += chip_stack.chip_count

            if total:
                location = (config.player_chip_stack_location.x +
                            i * (config.chip_size + config.chip_spacing) -
                            0.5 * config.chip_size,
                            config.player_chip_stack_location.y +
                            2.5 * config.chip_size,
                            config.chip_size, config.chip_size)

                draw_text(
                    location,
                    str(total),
                    player_order=self.player_order,
                    text_colour=chip_stack.chip.colour
                )
