from itertools import combinations
from random import shuffle

from data import raw_tile_data, raw_card_data
from chip_types import ChipType
from colour_count import ColourCount, ChipStacks, PlayerChipStack, \
    PlayerCardStack
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

    def __iter__(self):
        return iter(self.components)

    def __len__(self):
        return len(self.components)

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

    def _filter_by_player(self, player):
        return ComponentDatabase(
            [c for c in self.components
             if c.state == ComponentStates.in_player_area and
             c.player == player]
        )

    def filter(self, state=None, component_class=None, card_face_up=None,
               card_row=None, chip_type=None, player=None):
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
        if player is not None:
            result = result._filter_by_player(player)
        return result

    def count_for_colour(self, chip_type):
        return sum(1 for c in self.components
                   if c.chip_type == chip_type)

    def count_by_colour(self, result_class=ColourCount):
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
    def table_card_grid(self):
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
        card_grid = self.table_card_grid
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

    @property
    def top_table_chips(self):
        # Actual chips on top of each chip stack
        return [self.chip_from_supply(chip_type) for chip_type in self.table_chips]

    def chip_from_supply(self, chip_type):
        try:
            return self.chips_from_supply(chip_type)[0]
        except IndexError:
            return None
        # return self.filter(state=ComponentStates.in_supply, component_class=Chip, chip_type=chip_type).components[0]

    def chips_from_supply(self, chip_type):
        return self.filter(state=ComponentStates.in_supply, component_class=Chip, chip_type=chip_type).components

    def chip_count_for_player(self, player):
        return self.filter(
            state=ComponentStates.in_player_area,
            component_class=Chip,
            player=player
        ).count_by_colour(PlayerChipStack)

    def card_reward_for_player(self, player):
        return self.filter(
            state=ComponentStates.in_player_area,
            component_class=Card,
            player=player
        ).count_by_colour(PlayerCardStack)

    @property
    def table_card_stacks(self):
        return self.filter(
            state=ComponentStates.in_supply, component_class=Card, card_face_up=False
        ).count_by_row()

    @property
    def table_open_cards(self):
        return self.filter(
            state=ComponentStates.in_supply, component_class=Card, card_face_up=True
        )

    @property
    def holding_area_components(self):
        return self.filter(
            state=ComponentStates.in_holding_area
        )

    @property
    def holding_area_chips(self):
        return self.filter(
            state=ComponentStates.in_holding_area, component_class=Chip
        )

    @property
    def holding_area_cards(self):
        return self.filter(
            state=ComponentStates.in_holding_area, component_class=Card
        )

    @property
    def table_tiles(self):
        return self.filter(
            state=ComponentStates.in_supply, component_class=Tile
        )

    @property
    def is_empty(self):
        return len(self) == 0

    def valid_moves(self, current_player):
        """
        list of Move objects, each containing the pieces which the current
        player could take/buy/reserve
        """
        result = []

        # 3 different chips, if available
        top_table_chips = [c for c in self.top_table_chips if c.chip_type != ChipType.yellow_gold]
        if len(top_table_chips) >= 3:
            result += [Move(pieces=list(c), move_type=MoveType.take_different_chips) for c in combinations(top_table_chips, 3)]

        # 2 different chips, if 2 available but not 3
        elif len(top_table_chips) == 2:
            result.append(Move(pieces=top_table_chips, move_type=MoveType.take_different_chips))

        # 1 single chip, if chips of only 1 type available and less than 4 of that type
        elif len(top_table_chips) == 1 and len(self.chips_from_supply(top_table_chips[0])) < 4:
            result.append(Move(pieces=top_table_chips, move_type=MoveType.take_different_chips))

        for chip_type, chip_count in self.table_chips.items():
            if chip_type != ChipType.yellow_gold and chip_count >= 3:
                result.append(Move(
                    pieces=self.chips_from_supply(chip_type)[:2],
                    move_type=MoveType.take_same_chips
                ))

        result += [Move(pieces=[card], move_type=MoveType.buy_card)
                   for card in self.table_open_cards
                   if self.filter(
                state=ComponentStates.in_player_area,
                player=current_player
            ).count_by_colour().covers_cost(card.chip_cost)]

        return result

    def valid_pieces(self, current_player):
        valid_moves = self.valid_moves(current_player)
        pieces_taken = self.filter(state=ComponentStates.in_holding_area)

        # Nothing taken yet, all moves are still possible
        if not pieces_taken:
            return sum([m.pieces for m in valid_moves], [])

        # TODO Any more Pythonic way of doing the following?
        # Some pieces taken, only allow moves which include the ones which have been taken
        result = set()
        for valid_move in valid_moves:
            pieces_remaining = list(valid_move.pieces)
            for taken in pieces_taken:
                found = False
                for i, remaining in enumerate(pieces_remaining):
                    if pieces_match(taken, remaining):
                        del (pieces_remaining[i])
                        found = True
                        continue
                if not found:
                    # Can't find this piece, so no longer a valid move
                    pieces_remaining = []
                    continue
            for piece in pieces_remaining:
                result.add(piece)
        return result

    def is_valid_action(self, current_player, component):
        valid_pieces = self.valid_pieces(current_player)
        if component in valid_pieces:
            return True

        if not isinstance(component, Chip):
            return False

        # When taking the second chip of the same colour, the piece in valid_pieces
        # is actually the one which is now in the holding area
        # So just check whether it is the same type
        return any(c.chip_type == component.chip_type for c in valid_pieces)

    def turn_complete(self, current_player):
        return len(self.valid_pieces(current_player)) == 0

    # TODO: Better place for this? Maybe not in the main 'database' - too specific
    def pay_chip_cost(self, chip_cost, player):
        player_chips = self.filter(state=ComponentStates.in_player_area, component_class=Chip, player=player)
        card_rewards = self.filter(state=ComponentStates.in_holding_area, component_class=Card, player=player).\
            count_by_colour()

        yellow_needed = 0
        for chip_type in chip_cost:
            chips_needed = chip_cost.colour_count[chip_type]
            if chip_type in card_rewards:
                chips_needed -= card_rewards.colour_count[chip_type]

            chips = player_chips.filter(chip_type=chip_type)
            for i in range(chips_needed):
                if i < len(chips):
                    chips.components[i].to_supply()
                else:
                    yellow_needed += 1

        for _ in range(yellow_needed):
            chip = player_chips.chip_from_supply(ChipType.yellow_gold)
            chip.to_supply()


# TODO: Move to a better place?
def pieces_match(a, b):
    if a == b:
        return True
    return isinstance(a, Chip) and isinstance(b, Chip) and a.chip_type == b.chip_type
