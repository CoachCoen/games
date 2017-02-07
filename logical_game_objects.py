from enum import Enum
from random import shuffle

from physical_game_objects import DrawCard, DrawCardRow, \
    DrawCentralTableArea, DrawTable, DrawCardCost
from data import raw_starter_decks


class JewelType(Enum):
    green_emerald = 1
    blue_sapphire = 2
    red_ruby = 3
    white_diamond = 4
    black_onyx = 5
    yellow_gold = 6


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


class CardCost(AbstractGameObject, DrawCardCost):
    def __init__(self, raw_cost=""):
        self.cost = self.parse_raw_cost(raw_cost)

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

class Card(AbstractGameObject, DrawCard):
    def __init__(self, jewel_type, points=0, cost=""):
        self.cost = CardCost(cost)
        self.jewel_type = jewel_type
        self.points = points


class CardDeck(AbstractGameObject):
    def __init__(self, cards=None):
        self.cards = cards if cards else []


# class ChipStack(AbstractGameObject):
#     def __init__(self):
#         self.chips = []


class CardRow(AbstractGameObject, DrawCardRow):
    def __init__(self, row_number):
        self.card_deck = CardDeck(starter_deck(raw_starter_decks[row_number]))
        self.columns = [Card(jewel_type=JewelType.green_emerald,
                             points=2, cost="5 black, 3 red, 3 blue, 3 white")] * 4
        # self.columns = [] * 4


# class ChipStacksRow(AbstractGameObject):
#     def __init__(self):
#         self.stacks = {i: ChipStack() for i in JewelType}
#
#
# class NobleTilesRow(AbstractGameObject):
#     def __init__(self, player_count):
#         self.columns = [] * (player_count + 1)


class Player(AbstractGameObject):
    def __init__(self, name):
        self.name = name


class CentralTableArea(AbstractGameObject, DrawCentralTableArea):
    def __init__(self, player_count):
        # def __init__(self, player_count):
        # self.noble_tiles_row = NobleTilesRow(player_count)
        # self.chip_stacks_row = ChipStacksRow()
        self.card_rows = [CardRow(i) for i in range(3)]


class Table(AbstractGameObject, DrawTable):
    def __init__(self, players):
        self.players = [Player(name=p) for p in players]
        self.central_table_area = \
            CentralTableArea(player_count=self.player_count)

    @property
    def player_count(self):
        return len(self.players)
