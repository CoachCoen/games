from random import shuffle

from data import ChipType
from data import row_1, row_2, row_3

from settings import config

from drawing_surface import draw_rectangle, draw_pologon, draw_text, \
    draw_circle
from drawing_surface import ColourPalette


class AbstractFactory(object):
    pass


class AbstractGameComponent(object):
    def draw(self, x, y):
        """
        Draw this object at (x, y)
        :param x: x-location
        :param y: y-location
        """
        return NotImplemented


class Card(AbstractGameComponent):
    def __init__(self, chip_cost, reward_chip, points):
        self.chip_cost = chip_cost
        self.reward_chip = reward_chip
        self.points = points

    def draw(self, x, y):
        draw_rectangle((x, y, config.card_width, config.card_height),
                       ColourPalette.card_background)
        if self.points:
            draw_text(
                (x + config.points_location_x, y + config.points_location_y),
                str(self.points)
            )

        self.chip_cost.draw(
            x + config.cost_location_x,
            y + config.cost_location_y,
            scaling_factor=config.chip_cost_scaling
        )

        self.reward_chip.draw(
            x + config.reward_chip_x,
            y + config.reward_chip_y,
            scaling_factor=config.reward_chip_scaling
        )


class Chip(AbstractGameComponent):
    def __init__(self, chip_type, colour):
        self.chip_type = chip_type
        self.colour = colour

    def draw(self, x, y, scaling_factor=1, player_order=None):
        draw_circle(
            (x, y),
            int(config.chip_size * scaling_factor),
            self.colour,
            player_order=player_order
        )


class Tile(AbstractGameComponent):
    def __init__(self, chip_cost, points):
        self.chip_cost = chip_cost
        self.points = points

    def draw(self, x, y):
        draw_rectangle(
            (x, y, config.tile_size, config.tile_size),
            ColourPalette.card_background
        )
        self.chip_cost.draw(
            x + config.cost_location_x,
            y + config.cost_location_y,
            scaling_factor=config.chip_cost_scaling
        )
        draw_text(
            (x + config.points_location_x, y + config.points_location_y),
            str(self.points)
        )


class AbstractGameComponentCollection(object):
    pass


class ChipStack(AbstractGameComponentCollection):
    def __init__(self, chip, chip_count):
        self.chip = chip
        self.chip_count = chip_count

    def draw(self, x, y, scaling_factor=1, player_order=None):
        if self.chip_count:
            self.chip.draw(x, y, scaling_factor, player_order=player_order)
            draw_text(
                (x - 8, y - 12),
                str(self.chip_count),
                text_colour=self.chip.colour,
                reverse_colour=True,
                font_size=config.chip_font_size * scaling_factor,
                player_order=player_order
            )


class ChipStackCollection(AbstractGameComponentCollection):
    def __init__(self, chip_stacks):
        self.chip_stacks = chip_stacks

    def get_stack_for_chip_type(self, chip_type):
        for chip_stack in self.chip_stacks:
            if chip_stack.chip.chip_type == chip_type:
                return chip_stack
        return None

    def draw(self, x, y, scaling_factor=1):
        for i, chip_stack in enumerate(self.chip_stacks):
            chip_stack.draw(
                x,
                int(y + i * (config.chip_size * 2 + config.chip_spacing)
                    * scaling_factor),
                scaling_factor
            )


class CardDeck(AbstractGameComponentCollection):
    def __init__(self, cards):
        self.cards = cards
        shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

    def draw(self, x, y):
        draw_rectangle((x, y, config.card_width, config.card_height),
                       ColourPalette.card_deck_background)
        if len(self.cards):
            draw_text(
                (x + config.points_location_x, y + config.points_location_y),
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

    def shuffle_and_limit(self, count):
        shuffle(self.tiles)
        self.tiles = self.tiles[:count]

    @property
    def points(self):
        return sum(t.points for t in self.tiles)

    def draw(self, x, y):
        for i, tile in enumerate(self.tiles):
            tile.draw(
                x + i * (config.tile_size + config.tile_spacing),
                y
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
        draw_rectangle((0, 0, config.tabletop_width, config.tabletop_height),
                       ColourPalette.table_cloth)

    @staticmethod
    def _draw_player_corners():
        for (x, y) in [
            (0, 0),
            (0, config.tabletop_height),
            (config.tabletop_width, config.tabletop_height),
            (config.tabletop_width, 0)
        ]:
            draw_pologon([
                (x, abs(y - config.tabletop_height / 2.2)),
                (abs(x - config.tabletop_width / 2.2), y),
                (x, y)],
                ColourPalette.corners
            )

    def draw(self):
        self._draw_tablecloth()
        self._draw_player_corners()
        self.chip_stacks.draw(
            config.central_area_x + config.chip_stack_x,
            config.central_area_y + config.chip_stack_y
        )
        for i, card_deck in enumerate(self.card_decks):
            card_deck.draw(
                config.central_area_x + config.card_decks_location_x,
                config.central_area_y + config.card_decks_location_y +
                i * (config.card_height + config.card_spacing)
            )

        for i, card_row in enumerate(self.card_grid):
            for j, card in enumerate(card_row):
                card.draw(
                    config.central_area_x + config.card_decks_location_x +
                    (j + 1) * (config.card_width + config.card_spacing),
                    config.central_area_y + config.card_decks_location_y +
                    i * (config.card_height + config.card_spacing)
                )

        self.tiles.draw(
            config.central_area_x + config.tiles_row_x,
            config.central_area_y + config.tiles_row_y
        )


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
            chip_count, colour_name = stack_data.strip().split(" ")
            chip_stacks.append(
                ChipStack(
                    chip=self.component_factory('chip', colour_name),
                    chip_count=int(chip_count)
                )
            )
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
            card_grid.append([card_deck.pop() for _ in range(4)])

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


class Player(object):
    def __init__(self, name, player_order):
        self.name = name
        self.player_order = player_order

        component_collection_factory = ComponentCollectionFactory()
        self.cards = component_collection_factory('card', row_1)
        # self.cards = component_collection_factory('card', '')
        # TODO: Remove this when done testing showing the players' hands
        self.chip_stacks = component_collection_factory(
            'chip', '1 blue,1 white,1 black,1 green,1 red,1 yellow'
        )
        self.tiles = component_collection_factory('tile', '')

    @property
    def points(self):
        return self.cards.points + self.tiles.points

    # TODO: Refactor this - messy?
    def draw(self):
        draw_rectangle(
            (0, 0, config.player_area_width, config.player_area_height),
            player_order=self.player_order,
            colour=ColourPalette.player_area
        )
        draw_text(
            (config.player_name_x, config.player_name_y),
            self.name,
            player_order=self.player_order
        )
        if self.points:
            draw_text(
                (config.player_points_x, config.player_points_y),
                str(self.points),
                player_order=self.player_order
            )

        for i, chip_type in enumerate(ChipType):
            total = self.cards.count_for_reward_type(chip_type)
            chip_stack = self.chip_stacks.get_stack_for_chip_type(chip_type)

            if total:
                location = (
                    config.player_chip_stack_x +
                    i * (config.chip_size + config.chip_spacing) -
                    0.5 * config.chip_size,
                    config.player_chip_stack_y + config.chip_size,
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

            if chip_stack.chip_count:
                chip_stack.draw(
                    config.player_chip_stack_x +
                    i * (config.chip_size + config.chip_spacing),
                    config.player_chip_stack_y,
                    scaling_factor=config.chip_cost_scaling,
                    player_order=self.player_order
                )
                total += chip_stack.chip_count

            if total:
                location = (config.player_chip_stack_x +
                            i * (config.chip_size + config.chip_spacing) -
                            0.5 * config.chip_size,
                            config.player_chip_stack_y +
                            2.5 * config.chip_size,
                            config.chip_size, config.chip_size)

                draw_text(
                    location,
                    str(total),
                    player_order=self.player_order,
                    text_colour=chip_stack.chip.colour
                )


class Game(object):
    def __init__(self):
        self.table = None
        self.players = None

    @property
    def player_count(self):
        return len(self.players)

    def draw(self):
        self.table.draw()
        for player in self.players:
            player.draw()


class GameFactory(object):
    def __init__(self):
        pass

    def __call__(self, player_names):
        game = Game()

        game.players = [Player(name, i)
                        for (i, name) in enumerate(player_names)]
        table_factory = TableFactory()
        game.table = table_factory(game.player_count)

        return game
