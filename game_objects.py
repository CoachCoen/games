from random import shuffle

from data import raw_starter_decks
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
    def __init__(self, cost, output_chip, points):
        self.cost = cost
        self.output_chip = output_chip
        self.points = points

    def draw(self, x, y):
        draw_rectangle((x, y, config.card_width, config.card_height),
                       ColourPalette.card_background)
        if self.points:
            draw_text(
                (x + config.points_location_x, y + config.points_location_y),
                str(self.points)
            )

        self.cost.draw(x + config.cost_location_x, y + config.cost_location_y)

        draw_circle(
            (
                x + config.card_width - config.points_location_x,
                int(y + config.points_location_y + config.chip_size)
            ),
            int(config.chip_size * 1.5), self.jewel_type.value
        )


class Chip(AbstractGameComponent):
    def __init__(self, chip_type, colour):
        self.chip_type = chip_type
        self.colour = colour

    def draw(self, x, y):
        draw_circle((x, y), config.chip_size, self.colour)


class NoblesTile(AbstractGameComponent):
    def __init__(self, cost, points):
        self.cost = cost
        self.points = points

    def draw(self, x, y):
        draw_rectangle(
            (x, y, config.nobles_tile_size, config.nobles_tile_size),
            ColourPalette.card_background
        )
        self.cost.draw(x, y)


class AbstractGameComponentCollection(object):
    pass


class ChipStack(AbstractGameComponentCollection):
    def __init__(self, chip, chip_count):
        self.chip = chip
        self.chip_count = chip_count

    def draw(self, x, y):
        if self.chip_count:
            self.chip.draw(x, y)
            draw_text((x - 8, y - 12), str(self.chip_count),
                      text_colour=self.chip.colour, reverse_colour=True)


class ChipStackCollection(AbstractGameComponentCollection):
    def __init__(self, chip_stacks):
        self.chip_stacks = chip_stacks

    def draw(self, x, y):
        for i, chip_stack in enumerate(self.chip_stacks):
            chip_stack.draw(
                x + config.chip_stack_x,
                y + config.chip_stack_y + i *
                (config.chip_size * 2 + config.chip_spacing)
            )


class CardDeck(AbstractGameComponentCollection):
    def __init__(self, cards):
        self.cards = cards

    def draw(self, x, y):
        draw_rectangle((x, y, config.card_width, config.card_height),
                       ColourPalette.card_deck_background)
        if len(self.cards):
            draw_text(
                (x + config.points_location_x, y + config.points_location_y),
                str(len(self.cards))
            )


class CardDeckFactory():
    def __call__(self, raw_row):
        card_factory = CardFactory()
        cards = []
        for card_details in raw_row.split('\n'):
            if card_details:
                cards.append(card_factory(card_details))
        return CardDeck(cards)

# class CardRow(AbstractGameObject):
#     def __init__(self, row_number):
#         self.card_deck = CardDeck(starter_deck(raw_starter_decks[row_number]))
#         self.columns = \
#             [Card(jewel_type=JewelType.green_emerald,
#                   points=2, raw_cost="5 black, 3 red, 3 blue, 3 white")] * 4
#
#     def draw(self, x, y):
#         self.card_deck.draw(x, y)
#         for column, card in enumerate(self.columns):
#             card.draw(x + (column + 1) * config.column_width, y)
#
#
# class ChipStacksColumn(AbstractGameObject):
#     def __init__(self, chip_count):
#         self.stacks = [ChipStack(i, chip_count) for i in JewelType]
#
#     def draw(self, x, y):
#         for i, chip_stack in enumerate(self.stacks):
#             chip_stack.draw(
#                 x,
#                 y + i * (config.chip_stack_size * 2 +
#                          config.chip_stack_spacing)
#             )




# class NobleTilesRow(AbstractGameObject):
#     def __init__(self, player_count):
#         noble_tiles = nobles_deck()
#         shuffle(noble_tiles)
#         self.tiles = noble_tiles[:(player_count + 1)]
#
#     def draw(self, x, y):
#         for i, tile in enumerate(self.tiles):
#             tile.draw(
#                 x + i * (config.nobles_tile_size + config.nobles_tile_spacing),
#                 y
#             )




# class CentralTableArea(AbstractGameObject):
#     def __init__(self):
#         pass
#
    # def __init__(self, player_count):
        # def __init__(self, player_count):
        # TODO: Initialise with correct number of chips
        # self.chip_stacks_column = ChipStacksColumn(player_count)
        # self.card_rows = [CardRow(i) for i in range(3)]
        # self.noble_tiles_row = NobleTilesRow(player_count)

    # def draw(self, x, y):
    #     self.chip_stacks_column.draw(
    #         x + config.chip_stack_x,
    #         y + config.chip_stack_y
    #     )
    #     self.noble_tiles_row.draw(
    #         x + config.noble_tiles_row_x,
    #         y + config.noble_tiles_row_y
    #     )
    #     for (i, card_row) in enumerate(self.card_rows):
    #         card_row.draw(
    #             x + config.chip_stack_size * 2,
    #             y + i * config.row_height +
    #             config.nobles_tile_size + config.nobles_tile_spacing
    #         )


class Table(object):
    """
    Central playing area - shared space for all players
    Contains all game components, apart from what's in the players' hands
    """
    def __init__(self, chip_stack_set, card_decks):
        self.chip_stack_set = chip_stack_set
        # TODO Make consistent: stack_set and decks (deck_sets?)
        self.card_decks = card_decks
        # self.players = []
        # self.central_table_area = \
        #     CentralTableArea(player_count=self.player_count)

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
        self.chip_stack_set.draw(config.central_area_x, config.central_area_y)
        for i, card_deck in enumerate(self.card_decks):
            card_deck.draw(
                config.central_area_x + config.card_decks_location_x,
                config.central_area_y + config.card_decks_location_y +
                    i * (config.card_height + config.card_spacing)
            )
        # self.central_table_area.draw(config.central_area_x,
        #                              config.central_area_y)

    # def starter_deck(raw_row):
    #     """
    #     parses the raw_row data into a list of Card instances
    #
    #     :param raw_row: string with e.g.
    #         7 white: 1 blue, 4 points
    #         7 black: 1 white, 4 points
    #         7 blue: 1 green, 4 points
    #
    #     :return: [Card objects]
    #     """
    #
    #     # TODO: costs consist of count & type, reward consist of type
    #     # type is specified by a Chip(..) instance
    #
    #     deck = []
    #     for line in [l.strip() for l in raw_row.split("\n") if l.strip()]:
    #         deck.append(card_factory(raw_row))
    #
    #         # e.g. 7 white: 1 blue, 4 points
    #     shuffle(deck)
    #
    #     return deck
    #



class ChipFactory():
    def __call__(self, colour_name=None, chip_type=None):
        if colour_name:
            chip_type, colour = {
                'red': (ChipType.red_ruby, ColourPalette.red_chip),
                'blue': (ChipType.blue_sapphire, ColourPalette.blue_chip),
                'white': (ChipType.white_diamond, ColourPalette.white_chip),
                'green': (ChipType.green_emerald, ColourPalette.green_chip),
                'black': (ChipType.black_onyx, ColourPalette.black_chip),
                'yellow': (ChipType.yellow_gold, ColourPalette.yellow_chip)
            }[colour_name]

        colour = {
                ChipType.red_ruby: ColourPalette.red_chip,
                ChipType.blue_sapphire: ColourPalette.blue_chip,
                ChipType.white_diamond: ColourPalette.white_chip,
                ChipType.green_emerald: ColourPalette.green_chip,
                ChipType.black_onyx: ColourPalette.black_chip,
                ChipType.yellow_gold: ColourPalette.yellow_chip
            }[chip_type]
        return Chip(chip_type, colour)


class CardFactory():
    def __call__(self, card_details):
        return Card()
        # raw_cost, reward_text = card_details.split(':')
        #
        # # Not all cards give points
        # if "," in reward_text:
        #     # e.g. 5 black, 3 red, 3 black, 3 white: 1 blue, 3 points
        #     reward_chip, reward_points = reward_text.split(",")
        #     reward_chip = ChipStack()
        #     chip_factory(colour_name=reward_chip.split(" ")[1])
        #     reward_points = int(reward_points.strip().split(" ")[0])
        #
        # else:
        # # e.g. 7 white: 1 blue, 4 points
        #     reward_chip = chip_factory(colour_name=reward_text.split(" ")[1])
        #     reward_points = 0
        #
        # deck.append(
        #     card_factory()
        # Card(
        #     raw_cost=raw_cost,
        #     jewel_type=reward_chip,
        #     points=reward_points
        # ))




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

    def card_factory(self, details):
        pass

    def tile_factory(self, details):
        pass


class ChipStackSetFactory(AbstractFactory):
    def __call__(self, raw_stack_data):
        # e.g. "5 black, 3 red, 3 black, 3 white"
        # name_to_type = {
        #     'white': ChipType.white_diamond,
        #     'red': ChipType.red_ruby,
        #     'blue': ChipType.blue_sapphire,
        #     'black': ChipType.black_onyx,
        #     'green': ChipType.green_emerald,
        #     'yellow': ChipType.yellow_gold
        # }
        chip_stacks = []

        chip_factory = ChipFactory()
        for stack_data in raw_stack_data.split(","):
            chip_count, name = stack_data.strip().split(" ")
            # chip_type = name_to_type[name.strip()]
            chip_stacks.append(
                ChipStack(chip=chip_factory(name), chip_count=chip_count)
            )
        return ChipStackSet(chip_stacks)



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

        chip_factory = ChipFactory()
        for stack_data in raw_stack_data.split(","):
            chip_count, name = stack_data.strip().split(" ")
            # chip_type = name_to_type[name.strip()]
            chip_stacks.append(
                ChipStack(chip=chip_factory(name), chip_count=chip_count)
            )
        return ChipStackCollection(chip_stacks)


    def card_collection_factory(self, details):
        pass

    def tile_collection_factory(self, details):
        pass


class TableFactory():
    def __init__(self):
        # Create all the elements that come in the box
        # self.card_decks = ..
        self.chip_stacks = []

    # def deal(self, players):
    #     # Create the players, give them their hands

    def __call__(self, player_count):
        # table.players = [Player(name=p) for p in players]
        # self.deal(players=players)

        # Chips: 7 for 4 player, 5 for 3 player, 4 for 2 player
        # plus 5 gold
        component_collection_factory = ComponentCollectionFactory()

        raw_chips = {
            4: '7 white, 7 blue, 7 red, 7 green, 7 black, 5 yellow',
            3: '5 white, 5 blue, 5 red, 5 green, 5 black, 5 yellow',
            2: '4 white, 4 blue, 4 red, 4 green, 4 black, 5 yellow',
        }[player_count]

        # chip_stack_set_factory = ChipStackSetFactory()
        # chip_stack_set = chip_stack_set_factory(raw_chip_set)

        chip_stacks = component_collection_factory('chip', raw_chips)

        # card_deck_factory = CardDeckFactory()
        card_decks = []
        for raw_cards in (row_1, row_2, row_3):
            card_decks.append(component_collection_factory('card', raw_cards))

        table = Table(chip_stacks=chip_stacks, card_decks=card_decks)
        return table


class Player(AbstractGameObject):
    def __init__(self, name):
        self.name = name


class Game(object):
    def __init__(self):
        self.table = None
        self.players = None

    @property
    def player_count(self):
        return len(self.players)

    def draw(self):
        self.table.draw()


class GameFactory(object):
    def __init__(self):
        pass

    def __call__(self, player_names):
        game = Game()

        game.players = [Player(name) for name in player_names]
        table_factory = TableFactory()
        game.table = table_factory(game.player_count)

        return game
