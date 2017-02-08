from random import shuffle

from data import raw_starter_decks
from data import JewelType

from settings import config

from drawing_surface import draw_rectangle, draw_pologon, draw_text, \
    draw_circle
from drawing_surface import ColourPalette


def starter_deck(raw_row):
    # TODO: Refactor this

    deck = []
    for line in [l.strip() for l in raw_row.split("\n") if l.strip()]:
        cost_text, reward_text = line.split(':')
        cost = []
        if "," in reward_text:
            reward_chip, reward_points = reward_text.split(",")
            reward_chip = Chip(jewel_type=[reward_chip.split(" ")[1]])
            reward_points = int(reward_points.strip().split(" ")[0])
        else:
            reward_chip = Chip(jewel_type=[reward_text.split(" ")[1]])
            reward_points = 0
        deck.append(Card(
            jewel_type=reward_chip,
            points=reward_points
        ))

    shuffle(deck)

    return deck


class AbstractGameObject(object):
    pass


# class NoblesTile(AbstractGameObject):
#     def __init__(self, cost, points):
#         self.cost = cost
#         self.points = points
#
#
class Chip(AbstractGameObject):
    def __init__(self, jewel_type):
        self.jewel_type = jewel_type


class CardCost(AbstractGameObject):
    def __init__(self, raw_cost=""):
        self.cost = self.parse_raw_cost(raw_cost)

    def draw(self, x, y):
        # TODO Tidy layout
        for (i, (jewel_type, number)) in \
                enumerate([(jewel_type, number)
                           for (jewel_type, number)
                           in self.cost.items() if number]):
            location = (x, y + (i * (config.chip_size + config.chip_spacing)))
            draw_circle(location, config.chip_size, jewel_type.value)

            location = (x + config.chip_size, y + ((i - 0.3) * (config.chip_size + config.chip_spacing)))
            # TODO Choose a contrasting colour for the number
            draw_text(location, str(number), font_size=18)

    def parse_raw_cost(self, raw_cost):
        # e.g. "5 black, 3 red, 3 black, 3 white"
        name_to_type = {
            'white': JewelType.white_diamond,
            'red': JewelType.red_ruby,
            'blue': JewelType.blue_sapphire,
            'black': JewelType.black_onyx,
            'green': JewelType.green_emerald
        }

        cost = {i: 0 for i in JewelType if i != JewelType.yellow_gold}

        for cost_item in raw_cost.strip().split(","):
            if not cost_item:
                continue
            n, c = cost_item.strip().split(" ")
            jewel_type = name_to_type[c.strip()]
            cost[jewel_type] = int(n)
            # cost.append([Chip(jewel_type=jewel_type)] * int(n))
        return cost

class Card(AbstractGameObject):
    def __init__(self, jewel_type, points=0, cost=""):
        self.cost = CardCost(cost)
        self.jewel_type = jewel_type
        self.points = points

    def draw(self, x, y):
        draw_rectangle((x, y, config.card_width, config.card_height),
                       ColourPalette.card_background)
        if self.points:
            draw_text((x + config.points_location_x, y + config.points_location_y),
                      str(self.points))

        self.cost.draw(x + config.cost_location_x, y + config.cost_location_y)

        # TODO Better variable name - top row?, top row left, top row right?
        draw_circle((x + config.card_width - config.points_location_x,
                     int(y + config.points_location_y + config.chip_size * 0.5)),
                    int(config.chip_size * 1.5), self.jewel_type.value)


class CardDeck(AbstractGameObject):
    def __init__(self, cards=None):
        self.cards = cards if cards else []

    def draw(self, x, y):
        draw_rectangle((x, y, config.card_width, config.card_height),
                       ColourPalette.card_deck_background)
        if len(self.cards):
            draw_text((x + config.points_location_x, y + config.points_location_y),
                      str(len(self.cards)))


class ChipStack(AbstractGameObject):
    def __init__(self, jewel_type, chip_count):
        self.jewel_type = jewel_type
        self.chip_count = chip_count

    def draw(self, x, y):
        if self.chip_count:
            draw_circle((x, y), config.chip_stack_size, self.jewel_type.value)
            # TODO Tidy up these parameters, calculate/into-config for (8, 12) offset
            draw_text((x - 8, y - 12), str(self.chip_count),
                      text_colour=self.jewel_type.value, reverse_colour=True)


class CardRow(AbstractGameObject):
    def __init__(self, row_number):
        self.card_deck = CardDeck(starter_deck(raw_starter_decks[row_number]))
        self.columns = [Card(jewel_type=JewelType.green_emerald,
                             points=2, cost="5 black, 3 red, 3 blue, 3 white")] * 4

    def draw(self, x, y):
        self.card_deck.draw(x, y)
        for column, card in enumerate(self.columns):
            card.draw(x + (column + 1) * config.column_width, y)


class ChipStacksColumn(AbstractGameObject):
    def __init__(self, chip_count):
        self.stacks = [ChipStack(i, chip_count) for i in JewelType]

    def draw(self, x, y):
        for i, chip_stack in enumerate(self.stacks):
            chip_stack.draw(x, y + i * (config.chip_stack_size + config.chip_stack_spacing))

#
#
# class NobleTilesRow(AbstractGameObject):
#     def __init__(self, player_count):
#         self.columns = [] * (player_count + 1)


class Player(AbstractGameObject):
    def __init__(self, name):
        self.name = name


class CentralTableArea(AbstractGameObject):
    def __init__(self, player_count):
        # def __init__(self, player_count):
        # self.noble_tiles_row = NobleTilesRow(player_count)
        # TODO: Initialise with correct number of chips
        self.chip_stacks_column = ChipStacksColumn(player_count)
        self.card_rows = [CardRow(i) for i in range(3)]

    def draw(self, x, y):
        self.chip_stacks_column.draw(x + config.chip_stack_x, y + config.chip_stack_y)
        for (i, card_row) in enumerate(self.card_rows):
            card_row.draw(x + config.chip_stack_size, y + i * config.row_height)


class Table(AbstractGameObject):
    def __init__(self, players):
        self.players = [Player(name=p) for p in players]
        self.central_table_area = \
            CentralTableArea(player_count=self.player_count)

    @property
    def player_count(self):
        return len(self.players)

    def _draw_tablecloth(self):
        draw_rectangle((0, 0, config.tabletop_width, config.tabletop_height),
                       ColourPalette.table_cloth)

    def _draw_player_corners(self):
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
        self.central_table_area.draw(config.central_area_x,
                                     config.central_area_y)

