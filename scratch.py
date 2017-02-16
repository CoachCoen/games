from random import shuffle

from data import raw_starter_decks
from data import JewelType

from settings import config

from drawing_surface import draw_rectangle, draw_pologon, draw_text, \
    draw_circle
from drawing_surface import ColourPalette


class AbstractGameObject(object):
    def draw(self, x, y):
        """
        Draw this object at (x, y)
        :param x: x-location
        :param y: y-location
        """
        return NotImplemented


class Chip(AbstractGameObject):
    def __init__(self, jewel_type, colour):
        self.jewel_type = jewel_type
        self.colour = colour

    # def draw(self, x, y):
    #     pass


# def chip_factory(colour_name=None, jewel_type=None):
#     if colour_name:
#         jewel_type, colour = {
#             'red': (JewelType.red_ruby, ColourPalette.red_chip),
#             'blue': (JewelType.blue_sapphire, ColourPalette.blue_chip),
#             'white': (JewelType.white_diamond, ColourPalette.white_chip),
#             'green': (JewelType.green_emerald, ColourPalette.green_chip),
#             'black': (JewelType.black_onyx, ColourPalette.black_chip),
#             'yellow': (JewelType.yellow_gold, ColourPalette.yellow_chip)
#         }[colour_name]
#
#     colour = {
#             JewelType.red_ruby: ColourPalette.red_chip,
#             JewelType.blue_sapphire: ColourPalette.blue_chip,
#             JewelType.white_diamond: ColourPalette.white_chip,
#             JewelType.green_emerald: ColourPalette.green_chip,
#             JewelType.black_onyx: ColourPalette.black_chip,
#             JewelType.yellow_gold: ColourPalette.yellow_chip
#         }[jewel_type]
#     return Chip(jewel_type, colour)

class ChipStack(AbstractGameObject):
    # def __init__(self, jewel_type, chip_count):
    #     self.chip = chip_factory(jewel_type=jewel_type)
    #     self.chip_count = chip_count

    def __init__(self, chip_type, chip_count):
        self.chip_type = chip_type
        self.chip_count = chip_count

    # def draw(self, x, y):
    #     if self.chip_count:
    #         self.chip.draw(x, y)
    #         # draw_circle((x, y), config.chip_stack_size, self.jewel_type.value)
    #         # TODO Tidy this up
    #         draw_text((x - 8, y - 12), str(self.chip_count),
    #                   text_colour=self.jewel_type.value, reverse_colour=True)


class ChipSet(AbstractGameObject):
    def __init__(self, chip_stacks):
        self.chip_stacks = chip_stacks

# class Cost(AbstractGameObject):
#     def __init__(self):
#         self.cost = []
#
#     def draw(self, x, y):
#         for i, chip_stack in enumerate(self.cost):
#             chip_stack.draw(
#                 x + (config.chip_size * 2 + config.chip_spacing), y
#             )

        # TODO Tidy layout
        # for (i, (jewel_type, number)) in \
        #         enumerate([(jewel_type, number)
        #                    for (jewel_type, number)
        #                    in self.cost.items() if number]):
        #     location = (
        #         x,
        #         y + (i * (config.chip_size * 2 + config.chip_spacing))
        #     )
        #     draw_circle(location, config.chip_size, jewel_type.value)
        #
        #     location = (
        #         x + config.chip_size * 2,
        #         y + (i - 0.3) * (config.chip_size * 2 + config.chip_spacing)
        #         - 2
        #     )
        #     # TODO Choose a contrasting colour for the number
        #     draw_text(location, str(number), font_size=18)

# def cost_factory(raw_cost):
#     @staticmethod
#     def parse_raw_cost(raw_cost):
#         # e.g. "5 black, 3 red, 3 black, 3 white"
#         name_to_type = {
#             'white': JewelType.white_diamond,
#             'red': JewelType.red_ruby,
#             'blue': JewelType.blue_sapphire,
#             'black': JewelType.black_onyx,
#             'green': JewelType.green_emerald
#         }
#
#         # cost = {i: 0 for i in JewelType if i != JewelType.yellow_gold}
#
#         cost = []
#         for cost_item in raw_cost.strip().split(","):
#             if not cost_item:
#                 continue
#
#             n, c = cost_item.strip().split(" ")
#             jewel_type = name_to_type[c.strip()]
#             cost.append(chip_factory())
#             cost[jewel_type] = int(n)
#         return cost

class Card(AbstractGameObject):
    def __init__(self, cost, output_chip, points):
        self.cost = cost
        self.output_chip = output_chip
        self.points = points
    # def __init__(self, jewel_type, points=0, raw_cost=""):
    #     self.cost = CardCost(raw_cost)
    #     self.jewel_type = jewel_type
    #     self.points = points

    # def draw(self, x, y):
    #     draw_rectangle((x, y, config.card_width, config.card_height),
    #                    ColourPalette.card_background)
    #     if self.points:
    #         draw_text(
    #             (x + config.points_location_x, y + config.points_location_y),
    #             str(self.points)
    #         )
    #
    #     self.cost.draw(x + config.cost_location_x, y + config.cost_location_y)
    #
    #     # TODO Better variable name - top row?, top row left, top row right?
    #     draw_circle(
    #         (
    #             x + config.card_width - config.points_location_x,
    #             int(y + config.points_location_y + config.chip_size)
    #         ),
    #         int(config.chip_size * 1.5), self.jewel_type.value
    #     )


# def card_factory(card_description):
#     raw_cost, reward_text = line.split(':')
#
#     # Not all cards give points
#     if "," in reward_text:
#         # e.g. 5 black, 3 red, 3 black, 3 white: 1 blue, 3 points
#         reward_chip, reward_points = reward_text.split(",")
#         reward_chip = ChipStack()
#         chip_factory(colour_name=reward_chip.split(" ")[1])
#         reward_points = int(reward_points.strip().split(" ")[0])
#
#     else:
#     # e.g. 7 white: 1 blue, 4 points
#         reward_chip = chip_factory(colour_name=reward_text.split(" ")[1])
#         reward_points = 0
#
#     deck.append(
#         card_factory()
#     Card(
#         raw_cost=raw_cost,
#         jewel_type=reward_chip,
#         points=reward_points
#     ))






class CardDeck(AbstractGameObject):
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    # def draw(self, x, y):
    #     draw_rectangle((x, y, config.card_width, config.card_height),
    #                    ColourPalette.card_deck_background)
    #     if len(self.cards):
    #         draw_text(
    #             (x + config.points_location_x, y + config.points_location_y),
    #             str(len(self.cards))
    #         )




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


class NoblesTile(AbstractGameObject):
    def __init__(self, cost, points):
        self.cost = cost
        self.points = points
    # def __init__(self, raw_cost, points):
    #     self.cost = CardCost(raw_cost)
    #
    #     # TODO Tidy up nested call
    #     # self.cost.cost = cost
    #     self.points = points

    # def draw(self, x, y):
    #     draw_rectangle(
    #         (x, y, config.nobles_tile_size, config.nobles_tile_size),
    #         ColourPalette.card_background
    #     )
    #     # self.cost.draw(x, y)


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




class CentralTableArea(AbstractGameObject):
    def __init__(self):
        pass

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


class Table(AbstractGameObject):
    def __init__(self):
        pass
        # self.players = []
        # self.central_table_area = \
        #     CentralTableArea(player_count=self.player_count)

    # @property
    # def player_count(self):
    #     return len(self.players)
    #
    # @staticmethod
    # def _draw_tablecloth():
    #     draw_rectangle((0, 0, config.tabletop_width, config.tabletop_height),
    #                    ColourPalette.table_cloth)

    # @staticmethod
    # def _draw_player_corners():
    #     for (x, y) in [
    #         (0, 0),
    #         (0, config.tabletop_height),
    #         (config.tabletop_width, config.tabletop_height),
    #         (config.tabletop_width, 0)
    #     ]:
    #         draw_pologon([
    #             (x, abs(y - config.tabletop_height / 2.2)),
    #             (abs(x - config.tabletop_width / 2.2), y),
    #             (x, y)],
    #             ColourPalette.corners
    #         )
    #
    # def draw(self):
    #     self._draw_tablecloth()
    #     self._draw_player_corners()
    #     self.central_table_area.draw(config.central_area_x,
    #                                  config.central_area_y)

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
        raw_chip_set = {
            4: '7 white, 7 blue, 7 red, 7 green, 7 black, 5 gold',
            3: '5 white, 5 blue, 5 red, 5 green, 5 black, 5 gold',
            2: '4 white, 4 blue, 4 red, 4 green, 4 black, 5 gold',
        }[player_count]
        chip_set = chip_set_factory(raw_chip_set)

        table = Table(chip_set=chip_set)
        return table


