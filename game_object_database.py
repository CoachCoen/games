from itertools import combinations
from random import shuffle

from data import raw_tile_data, raw_card_data
from chip_types import ChipType
from colour_count import ColourCount, ChipStacks
from game_objects import Chip, Card, Tile

from embody import EmbodyCardGridMixin, EmbodyCardDeckCountMixin, \
    EmbodyComponentDatabaseMixin

from states import PlayerStates, ComponentStates
from game_objects import Card
from moves_and_rules import Move, MoveType


class CardGrid(EmbodyCardGridMixin):
    def __init__(self, card_grid):
        self.card_grid = card_grid


class CardDeckCount(EmbodyCardDeckCountMixin):
    def __init__(self, card_deck_count):
        self.card_deck_count = card_deck_count


class ComponentDatabase(EmbodyComponentDatabaseMixin):
    def __init__(self, components=None):
        self.components = components if components is not None else []

    def init_components(self, player_count, component_collection_factory):

        self.components += component_collection_factory('card', raw_card_data)

        tiles = component_collection_factory('tile', raw_tile_data)
        shuffle(tiles)
        tiles = tiles[:player_count + 1]
        for i, tile in enumerate(tiles):
            tile.column = i
        self.components += tiles

        self.components += \
            component_collection_factory(
                'chip',
                {
                    4: '7 white, 7 blue, 7 red, 7 green, 7 black, 5 yellow',
                    3: '5 white, 5 blue, 5 red, 5 green, 5 black, 5 yellow',
                    2: '4 white, 4 blue, 4 red, 4 green, 4 black, 5 yellow',
                }[player_count]
            )

        # Shuffle the cards and the nobles
        # This also shuffles the tiles, but that doesn't matter
        shuffle(self.components)
        self.draw_cards()

    def _filter_by_state(self, state):
        return ComponentDatabase(
            [c for c in self.components
             if c.state == state])

    def _filter_by_class(self, component_class):
        return ComponentDatabase(
            [c for c in self.components
             if isinstance(c, component_class)]
        )

    def _filter_by_card_face_up(self, card_face_up):
        return ComponentDatabase(
            [c for c in self.components
             if c.face_up == card_face_up]
        )

    def _filter_by_card_row(self, card_row):
        return ComponentDatabase(
            [c for c in self.components
             if c.row == card_row]
        )

    def _filter_by_chip_type(self, chip_type):
        return ComponentDatabase(
            [c for c in self.components
             if c.chip_type == chip_type]
        )

    def filter(self, state=None, component_class=None, card_face_up=None,
               card_row=None, chip_type=None):
        result = self
        if state is not None:
            result = result._filter_by_state(state)
        if component_class is not None:
            result = result._filter_by_class(component_class)
        if card_face_up is not None:
            result = result._filter_by_card_face_up(card_face_up)
        if card_row is not None:
            result = result._filter_by_card_row(card_row)
        if chip_type is not None:
            result = result._filter_by_chip_type(chip_type)
        return result

    def count_for_colour(self, chip_type):
        return sum(1 for c in self.components
                   if c.chip_type == chip_type)

    def count_by_colour(self, result_class):
        return result_class({
            chip_type: self.count_for_colour(chip_type) for chip_type in ChipType
        })

    def count_by_row(self):
        return CardDeckCount({
            i: sum(1 for c in self.components if c.row == i) for i in range(3)
        })

    def as_grid(self):
        """
        3 rows for 4 cells each
        """
        result = [[None] * 4, [None] * 4, [None] * 4]

        for c in self.components:
            result[c.row][c.column] = c

        return CardGrid(result)

    @property
    def card_grid(self):
        return self.filter(
            state=ComponentStates.in_supply, component_class=Card, card_face_up=True
        ).as_grid()

    def draw_card_for_row(self, row, column):
        card_deck = self.filter(state=ComponentStates.in_supply, component_class=Card, card_face_up=False, card_row=row)
        if card_deck:
            card = card_deck.components[0]
            card.face_up = True
            card.column = column

    def draw_cards(self):
        card_grid = self.card_grid
        for row in range(3):
            for j in range(4):
                if card_grid.card_grid[row][j] is None:
                    self.draw_card_for_row(row, j)

    @property
    def table_chips(self):
        # Chip stacks on the table
        return self.filter(
            state=ComponentStates.in_supply, component_class=Chip
        ).count_by_colour(ChipStacks).filter(remove_blanks=True)

    def chip_from_supply(self, chip_type):
        return self.filter(state=ComponentStates.in_supply, component_class=Chip, chip_type=chip_type).components[0]

    @property
    def table_card_stacks(self):
        return self.filter(
            state=ComponentStates.in_supply, component_class=Card, card_face_up=False
        ).count_by_row()

    @property
    def table_tiles(self):
        return self.filter(
            state=ComponentStates.in_supply, component_class=Tile
        )

    def valid_moves(self, current_player):
        """
        list of Move objects, each containing the pieces which the current
        player could take/buy/reserve
        """
        result = []

        table_chips = self.table_chips
        if len(table_chips) > 3:
            result += [Move(pieces=c, move_type=MoveType.take_different_chips) for c in combinations(table_chips, 3)]

        return result

    def valid_pieces(self, current_player):
        valid_moves = self.valid_moves(current_player)
        return sum([m.pieces for m in valid_moves], ())
        # for
        # return set([p for p in [m.pieces for m in valid_moves])
