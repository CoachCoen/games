from random import choice, shuffle
from enum import Enum

from game_pieces import NobelsTile, Card, Chip, JewelType

class Row(Enum):
    # Make up for Python's zero-based indexes
    one = 0
    two = 1
    three = 2

def all_cards():
    row_1 = """
    3 red: 1 green
    3 black: 1 blue
    3 blue: 1 white
    3 green: 1 black
    3 white: 1 red

    4 red: 1 blue, 1 point
    4 black: 1 green, 1 point
    4 blue: 1 black, 1 point
    4 green: 1 green, 1 point
    4 white: 1 red, 1 point

    1 green, 2 blue: 1 red
    1 red, 2 green: 1 black
    1 blue, 2 white: 1 green
    1 white, 2 black: 1 blue
    1 black, 2 red: 1 white

    2 blue, 2 black: 1 white
    2 white, 2 red: 1 red
    2 white, 2 green: 1 black
    2 blue, 2 red: 1 green
    2 green, 2 black: 1 blue

    1 blue, 2 red, 2 black: 1 green
    1 black, 2 white, 2 blue: 1 black
    1 green, 2 black, 2 white: 1 red
    1 white, 2 red, 2 green: 1 blue
    1 black, 2 blue, 2 green: 1 white

    1 blue, 1 red, 3 green: 1 blue
    1 white, 1 green, 3 blue: 1 green
    1 black, 1 green, 3 red: 1 black
    1 black, 1 blue, 3 white: 1 white
    1 white, 1 red, 3 black: 1 red

    1 red, 1 white, 1 blue, 1 black: 1 green
    1 green, 1 red, 1 white, 1 blue: 1 black
    1 black, 1 green, 1 red, 1 white: 1 blue
    1 blue, 1 black, 1 green, 1 red: 1 white
    1 white, 1 blue, 1 black, 1 green: 1 red

    1 red, 1 green, 1 white, 2 blue: 1 black
    1 red, 1 blue, 1 white, 2 black: 1 green
    1 red, 1 blue, 1 blue, 2 green: 1 white
    1 black, 1 blue, 1 green, 2 white: 1 red
    1 green, 1 white, 1 black, 2 red: 1 blue
    """

    row_2 = """
    5 red: 1 white, 2 points
    5 black: 1 red, 2 points
    5 green: 1 green, 2 points
    5 white: 1 black, 2 points
    5 blue: 1 blue, 2 points

    6 red: 1 red, 3 points
    6 black: 1 black, 3 points
    6 green: 1 green, 3 points
    6 white: 1 white, 3 points
    6 blue: 1 blue, 3 points

    3 black, 5 red: 1 white, 2 points
    3 blue, 5 white: 1 blue, 2 points
    3 green, 5 blue: 1 green, 2 points
    3 white, 5 black: 1 red, 2 points
    3 red, 5 green: 1 black, 2 points

    1 green, 2 black, 4 red: 1 white, 2 points
    1 white, 2 green, 4 blue: 1 red, 2 points
    1 blue, 2 red, 4 green: 1 black, 2 points
    1 red, 2 white, 4 black: 1 blue, 2 points
    1 black, 2 blue, 4 white: 1 green, 2 points

    2 red, 3 blue, 3 black: 1 red, 1 point
    2 blue, 3 green, 3 black: 1 blue, 1 point
    2 white, 3 blue, 3 red: 1 white, 1 point
    2 black, 3 white, 3 green: 1 black, 1 point
    2 green, 3 white, 3 red: 1 green, 1 point

    2 red, 2 black, 3 green: 1 white, 1 point
    2 blue, 2 green, 3 red: 1 blue, 1 point
    2 white, 2 black, 3 blue: 1 green, 1 point
    2 white, 2 red, 3 black: 1 red, 1 point
    2 blue, 2 green, 3 white: 1 black, 1 point
    """

    row_3 = """
    7 white: 1 blue, 4 points
    7 black: 1 white, 4 points
    7 blue: 1 green, 4 points
    7 green: 1 red, 4 points
    7 red: 1 black, 4 points

    3 white, 7 black: 1 white, 5 points
    3 blue, 7 white: 1 blue, 5 points
    3 black, 7 red: 1 black, 5 points
    3 red, 7 green: 1 red, 5 points
    3 green, 7 blue: 1 green, 5 points

    3 white, 3 red, 6 black: 1 white, 5 points
    3 green, 3 white, 6 blue: 1 green, 5 points
    3 black, 3 green, 6 red: 1 black, 5 points
    3 red, 3 blue, 6 green: 1 red, 5 points
    3 blue, 3 black, 6 white: 1 blue, 5 points

    5 black, 3 red, 3 black, 3 white: 1 blue, 3 points
    5 white, 3 red, 3 blue, 3 black: 1 green, 3 points
    5 red, 3 blue, 3 black, 3 green: 1 white, 3 points
    5 blue, 3 white, 3 black, 3 green: 1 red, 3 points
    5 green, 3 white, 3 red, 3 blue: 1 black, 3 points
    """

    name_to_type = {
                    'white': JewelType.white_diamond,
                    'red': JewelType.red_ruby,
                    'blue': JewelType.blue_sapphire,
                    'black': JewelType.black_onyx,
                    'green': JewelType.green_emerald
                     }

    # TODO: Refactor this

    result = []
    for cards, row in ((row_1, Row.one), (row_2, Row.two), (row_3, Row.three)):
        for line in [l.strip() for l in cards.split("\n") if l.strip()]:
            cost_text, reward_text = line.split(':')
            cost = []
            for cost_item in cost_text.strip().split(","):
                n, c = cost_item.strip().split(" ")
                jewel_type = name_to_type[c.strip()]
                cost.append([Chip(jewel_type=jewel_type)] * int(n))
            if "," in reward_text:
                reward_chip, reward_points = reward_text.split(",")
                reward_chip = Chip(jewel_type=[reward_chip.split(" ")[1]])
                reward_points = int(reward_points.strip().split(" ")[0])
            else:
                reward_chip = Chip(jewel_type=[reward_text.split(" ")[1]])
                reward_points = 0
            result.append(Card(
                cost=cost,
                jewel_type=reward_chip,
                row=row,
                points=reward_points
            ))

    shuffle(result)

    return result

def all_nobles():
    nobles = []

    for (cost_1, cost_2) in [
        (JewelType.blue_sapphire, JewelType.green_emerald),
        (JewelType.white_diamond, JewelType.red_ruby),
        (JewelType.black_onyx, JewelType.red_ruby),
        (JewelType.green_emerald, JewelType.red_ruby),
        (JewelType.black_onyx, JewelType.green_emerald),
        (JewelType.white_diamond, JewelType.black_onyx),
        (JewelType.blue_sapphire, JewelType.white_diamond)
    ]:
        nobles.append(NobelsTile(
            cost=[cost_1, cost_2] * 4,
            points=3
        ))

    for (cost_1, cost_2, cost_3) in [
        (JewelType.green_emerald, JewelType.blue_sapphire, JewelType.red_ruby),
        (JewelType.blue_sapphire, JewelType.green_emerald, JewelType.white_diamond),
        (JewelType.black_onyx, JewelType.red_ruby, JewelType.white_diamond),
        (JewelType.black_onyx, JewelType.red_ruby, JewelType.green_emerald),
        (JewelType.blue_sapphire, JewelType.white_diamond, JewelType.red_ruby),
        (JewelType.black_onyx, JewelType.red_ruby, JewelType.blue_sapphire),
        (JewelType.black_onyx, JewelType.white_diamond, JewelType.blue_sapphire)
    ]:
        nobles.append(NobelsTile(
            cost=[cost_1, cost_2, cost_3] * 3,
            points=3
        ))

    return nobles

def draw_nobles(number_to_draw):
    a = all_nobles()
    shuffle(a)
    return a[:number_to_draw]

def chips_for_player_count(player_count):
    """
    Chips: 7 for 4 player, 5 for 3 player, 4 for 2 player
    plus 5 gold
    :param player_count:
    :return:
    """
    normal_chip_count = {4: 7, 3: 5, 2: 4}[player_count]
    return [Chip(i) for i in JewelType
            if i != JewelType.yellow_gold] * normal_chip_count + \
           [Chip(JewelType.yellow_gold)] * 5


class PlayerState(object):
    def __init__(self):
        """
        Players start with nothing
        """
        self.chips = []
        self.cards = []
        self.noble_tiles = []

class TableState(object):
    """
    On the table, not counting the player areas, we have:

    6 piles of chips
    3 card decks
    3 rows of 4 cards each
    <player count + 1>  noble cards
    """
    def __init__(self):
        self.decks = {
            Row.one: [],
            Row.two: [],
            Row.three: []
        }

        # 3 rows with 4 empty spaces each
        self.rows = [[None] * 4] * 3

class GameState(object):
    def __init__(self, players):
        self.players = players
        self.cards = all_cards()
        self.nobles = draw_nobles(self.player_count + 1)
        self.chips = chips_for_player_count(self.player_count)
        self.first_player = choice(self.players)
        self.table_state = TableState()

    @property
    def player_count(self):
        return len(self.players)

    def _prepare_table(self, player_count):
        # Move cards to the table
        # TODO Coen: This looks messy - refactor this
        for (deck, row) in [
            (Row.one, 1),
            (Row.two, 2),
            (Row.three, 3)
        ]:
            self.table_state.decks[deck].append(
                [c for c in self.cards if c.row == row]
            )

        # Put out the cards from the decks
        for row in Row:
            for i in range(4):
                self.table_state.rows[row][i] = \
                    self.table_state.decks[row].pop()
