from random import shuffle

from data import ChipType
from data import row_1, row_2, row_3

from settings import config
from settings import Vector

from drawing_surface import draw_rectangle, draw_pologon, draw_text, \
    draw_circle
from drawing_surface import ColourPalette
from buttons import buttons
from holding_area import holding_area

from game_actions import TakeChip, ReturnChip, TakeCard, ReturnCard
from game_state import game_state

class AbstractFactory(object):
    pass


class AbstractGameComponent(object):
    pass


class Card(AbstractGameComponent):
    def __init__(self, chip_cost, reward_chip, points):
        self.chip_cost = chip_cost
        self.reward_chip = reward_chip
        self.points = points
        self.location = None
        self.source = None
        self.card_deck = None

    def embody(self, location, can_return=False):
        self.location = location
        action = ReturnCard(self, holding_area) if can_return \
            else TakeCard(self, holding_area)
        if self in game_state.valid_actions:
            buttons.add(
                self.location.to_rectangle(config.card_size),
                action
            ).embody()

        self._draw()

    def _draw(self):
        draw_rectangle(self.location.to_rectangle(config.card_size),
                       ColourPalette.card_background)
        if self.points:
            draw_text(self.location + config.points_location, str(self.points))

        self.chip_cost.embody(
            self.location + config.cost_location,
            scaling_factor=config.chip_cost_scaling
        )

        self.reward_chip.embody(
            self.location + config.reward_chip_location,
            scaling_factor=config.reward_chip_scaling
        )


class CardSlot(object):
    def __init__(self, card):
        self.card = card
        self.card.source = self
        self.location = None

    def embody(self, location):
        self.location = location
        if self.card:
            self.card.embody(self.location)


class Chip(AbstractGameComponent):
    def __init__(self, chip_type, colour, source=None):
        self.chip_type = chip_type
        self.colour = colour
        self.location = None
        self.source = source

    def copy(self):
        return Chip(self.chip_type, self.colour, self.source)

    # TODO Better way to handle scaling factor and player_order (context handler?)
    def embody(self, location, scaling_factor=1, player_order=None,
               can_click=False):
        self.location = location
        self._draw(scaling_factor, player_order)
        if can_click:
            buttons.add(
                circle_location_to_rectangle(
                    self.location, config.chip_size * scaling_factor
                ),
                ReturnChip(self, holding_area)
            )

    def _draw(self, scaling_factor=1, player_order=None):
        draw_circle(
            self.location,
            int(config.chip_size * scaling_factor),
            self.colour,
            player_order=player_order
        )


class Tile(AbstractGameComponent):
    def __init__(self, chip_cost, points):
        self.chip_cost = chip_cost
        self.points = points
        self.location = None

    def embody(self, location):
        self.location = location
        self._draw()
        self.chip_cost.embody(self.location + config.cost_location,
                              scaling_factor=config.chip_cost_scaling
                              )

    def _draw(self):
        draw_rectangle(
            self.location.to_rectangle(config.tile_size),
            ColourPalette.card_background
        )
        draw_text(self.location + config.points_location,
                  str(self.points)
                  )


class AbstractGameComponentCollection(object):
    pass


# TODO Move this somewhere more sensible
def circle_location_to_rectangle(location, size):
    return (location.x - size, location.y - size,
            2 * size, 2 * size)


class ChipStack(AbstractGameComponentCollection):
    def __init__(self, chip, chip_count):
        self.chip = chip

        # Remember where this came from,
        # so we can return it half way through a turn
        # self.chip.source = self
        self.chip_count = chip_count
        self.location = None

    def take_one(self):
        self.chip_count -= 1

    def add_one(self):
        self.chip_count += 1

    def embody(self, location, scaling_factor=1,
               player_order=None, can_click=False):
        self.location = location
        if self.chip_count:
            if can_click and self in game_state.valid_actions:
                buttons.add(
                    circle_location_to_rectangle(
                        self.location, config.chip_size * scaling_factor
                    ),
                    TakeChip(self, holding_area)
                ).embody()
            self.chip.embody(
                self.location,
                scaling_factor,
                player_order=player_order
            )

        self._draw(scaling_factor, player_order)

    def _draw(self, scaling_factor=1, player_order=None):
        if self.chip_count:
            draw_text(
                self.location - Vector(4, 8),
                str(self.chip_count),
                text_colour=self.chip.colour,
                reverse_colour=True,
                font_size=config.chip_font_size * scaling_factor,
                player_order=player_order
            )


class ChipStackCollection(AbstractGameComponentCollection):
    def __init__(self, chip_stacks):
        self.chip_stacks = chip_stacks
        self.location = None

    def empty(self):
        return all(c.chip_count == 0 for c in self.chip_stacks)

    def get_stack_for_chip_type(self, chip_type):
        for chip_stack in self.chip_stacks:
            if chip_stack.chip.chip_type == chip_type:
                return chip_stack
        return None

    def embody(self, location, scaling_factor=1, can_click=False):
        self.location = location
        for i, chip_stack in enumerate(self.chip_stacks):
            chip_stack.embody(
                self.location +
                Vector(0, i * (config.chip_size * 2 + config.chip_spacing)
                       * scaling_factor),
                scaling_factor=scaling_factor,
                can_click=can_click
            )


class CardDeck(AbstractGameComponentCollection):
    def __init__(self, cards):
        self.location = None
        self.cards = cards

        # Back reference, to make it easier to draw the next card
        for card in cards:
            card.card_deck = self
        shuffle(self.cards)

    def pop(self):
        return self.cards.pop() if self.cards else None

    def add(self, card):
        self.cards.append(card)

    def embody(self, location):
        self.location = location
        self._draw()

    def _draw(self):
        draw_rectangle(self.location.to_rectangle(config.card_size),
                       ColourPalette.card_deck_background)
        if len(self.cards):
            draw_text(
                self.location + config.points_location,
                str(len(self.cards))
            )

    def count_for_reward_type(self, chip_type):
        return sum([1 for c in self.cards
                    if c.reward_chip.chip_type == chip_type])

    @property
    def points(self):
        return sum(c.points for c in self.cards)


class TileCollection(AbstractGameComponentCollection):
    def __init__(self, tiles):
        self.tiles = tiles
        self.location = None

    def shuffle_and_limit(self, count):
        shuffle(self.tiles)
        self.tiles = self.tiles[:count]

    @property
    def points(self):
        return sum(t.points for t in self.tiles)

    def embody(self, location):
        self.location = location
        for i, tile in enumerate(self.tiles):
            tile.embody(
                self.location +
                Vector(i * (config.tile_size.x + config.tile_spacing), 0)
            )


class Table(object):
    """
    Central playing area - shared space for all players
    Contains all game components, apart from what's in the players' hands
    """
    def __init__(self, chip_stacks, card_decks, card_grid, tiles):
        self.chip_stacks = chip_stacks
        self.card_decks = card_decks
        self.card_grid = card_grid
        self.tiles = tiles
        # self.players = []

    # @property
    # def player_count(self):
    #     return len(self.players)
    #
    @staticmethod
    def _draw_tablecloth():
        draw_rectangle((0, 0) + tuple(config.tabletop_size),
                       ColourPalette.table_cloth)

    @staticmethod
    def _draw_player_corners():
        for (x, y) in [
            (0, 0),
            (0, config.tabletop_size.y),
            (config.tabletop_size.x, config.tabletop_size.y),
            (config.tabletop_size.x, 0)
        ]:
            draw_pologon([
                (x, abs(y - config.tabletop_size.x / 2.2)),
                (abs(x - config.tabletop_size.y / 2.2), y),
                (x, y)],
                ColourPalette.corners
            )

    def embody(self):
        self._draw()
        self.chip_stacks.embody(
            config.central_area_location +
            config.chip_stack_location,
            can_click=True,
        )
        for i, card_deck in enumerate(self.card_decks):
            card_deck.embody(config.central_area_location +
                             config.card_decks_location +
                             Vector(0, i * (config.card_size.y +
                                            config.card_spacing)))

        for i, card_row in enumerate(self.card_grid):
            for j, card_slot in enumerate(card_row):
                card_slot.embody(
                    config.central_area_location +
                    config.card_decks_location +
                    Vector(
                        (j + 1) * (config.card_size.x + config.card_spacing),
                        i * (config.card_size.y + config.card_spacing))
                )

        self.tiles.embody(
            config.central_area_location +
            config.tiles_row_location
        )

    def _draw(self):
        self._draw_tablecloth()
        self._draw_player_corners()


class ComponentFactory(AbstractFactory):
    def __call__(self, component_type, details):
        func = {
            'chip': self.chip_factory,
            'card': self.card_factory,
            'tile': self.tile_factory
        }[component_type]
        return func(details)

    @staticmethod
    def chip_factory(details):
        return Chip(*{
            'red': (ChipType.red_ruby, ColourPalette.red_chip),
            'blue': (ChipType.blue_sapphire, ColourPalette.blue_chip),
            'white': (ChipType.white_diamond, ColourPalette.white_chip),
            'green': (ChipType.green_emerald, ColourPalette.green_chip),
            'black': (ChipType.black_onyx, ColourPalette.black_chip),
            'yellow': (ChipType.yellow_gold, ColourPalette.yellow_chip)
        }[details])

    @staticmethod
    def card_factory(details):
        raw_cost, reward_text = details.split(':')

        if "," in reward_text:
            # e.g. 5 black, 3 red, 3 black, 3 white: 1 blue, 3 points
            raw_reward_chip, raw_reward_points = reward_text.split(",")
            reward_points = int(raw_reward_points)
        else:
            raw_reward_chip = reward_text
            reward_points = 0

        component_factory = ComponentFactory()
        reward_chip = component_factory('chip', raw_reward_chip)

        component_collection_factory = ComponentCollectionFactory()
        chip_cost = component_collection_factory('chip', raw_cost)

        return Card(
            chip_cost=chip_cost,
            reward_chip=reward_chip,
            points=reward_points
        )

    @staticmethod
    def tile_factory(details):
        raw_cost, raw_points = details.split(':')
        component_collection_factory = ComponentCollectionFactory()
        chip_cost = component_collection_factory('chip', raw_cost.strip())
        return Tile(chip_cost=chip_cost, points=int(raw_points))


class ComponentCollectionFactory(AbstractFactory):
    def __init__(self):
        self.component_factory = ComponentFactory()

    def __call__(self, component_type, details):
        func = {
            'chip': self.chip_collection_factory,
            'card': self.card_collection_factory,
            'tile': self.tile_collection_factory
        }[component_type]
        return func(details)

    def chip_collection_factory(self, details):
        chip_stacks = []

        for stack_data in details.split(","):
            if stack_data:
                chip_count, colour_name = stack_data.strip().split(" ")
                chip = self.component_factory('chip', colour_name)
                chip_stack = ChipStack(
                    chip=chip,
                    chip_count=int(chip_count)
                )
                chip.source = chip_stack
                chip_stacks.append(chip_stack)
        return ChipStackCollection(chip_stacks)

    def card_collection_factory(self, details):
        return CardDeck(
            [self.component_factory('card', card_details)
             for card_details in details.split('\n') if card_details]
        )

    def tile_collection_factory(self, details):
        return TileCollection([
                   self.component_factory('tile', details='%s:3' % raw_cost)
                   for raw_cost in details
                   ])


class TableFactory(object):
    def __call__(self, player_count):
        component_collection_factory = ComponentCollectionFactory()

        # 7 for 4 player, 5 for 3 player, 4 for 2 player plus 5 gold
        chip_stacks = component_collection_factory(
            'chip',
            {
                # TODO: Remove this, for testing only
                # 4: '1 white, 1 blue, 0 red, 0 green, 0 black, 5 yellow',
                4: '7 white, 7 blue, 7 red, 7 green, 7 black, 5 yellow',
                3: '5 white, 5 blue, 5 red, 5 green, 5 black, 5 yellow',
                2: '4 white, 4 blue, 4 red, 4 green, 4 black, 5 yellow',
            }[player_count]
        )

        card_decks = [
            component_collection_factory('card', raw_cards)
            for raw_cards in (row_1, row_2, row_3)
            ]

        card_grid = []
        for card_deck in card_decks:
            card_grid.append([CardSlot(card_deck.pop()) for _ in range(4)])

        tiles = component_collection_factory(
            'tile',
            [
                '4 blue, 4 green',
                '4 white, 4 red',
                '4 black, 4 red',
                '4 green, 4 red',
                '4 black, 4 green',
                '4 white, 4 black',
                '4 blue, 4 white',
                '3 green, 3 blue, 3 red',
                '3 blue, 3 green, 3 white',
                '3 black, 3 red, 3 white',
                '3 black, 3 red, 3 green',
                '3 blue, 3 white, 3 red',
                '3 black, 3 red, 3 blue',
                '3 black, 3 white, 3 blue'
            ]
        )
        tiles.shuffle_and_limit(player_count + 1)

        table = Table(
            chip_stacks=chip_stacks,
            card_decks=card_decks,
            card_grid=card_grid,
            tiles=tiles
        )
        return table
