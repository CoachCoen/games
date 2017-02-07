from random import choice, shuffle
from enum import Enum

from game_pieces import NobelsTile, Card, Chip, JewelType
from data import row_1, row_2, row_3

class Row(Enum):
    # Make up for Python's zero-based indexes
    one = 0
    two = 1
    three = 2


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
