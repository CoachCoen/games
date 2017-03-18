from itertools import combinations
from random import shuffle

from component_setup_data import raw_tile_data, raw_card_data
from chip_types import ChipType
from game_components import Chip, Card, Tile

from states import ComponentStates, PlayerStates
from game_move import Move, MoveType
from game import game
from utils import pieces_match, SplitIntoIncludedAndExcluded


class GameMechanics:
    def __init__(self):
        self._valid_moves = None

    @property
    def valid_actions(self):
        return self.valid_pieces(game.current_player)

    @property
    def player_count(self):
        """
        Some of the game rules depend on the number of players
        :return: Number of players
        """
        return len(game.players)

    def next_player(self):
        """
        Move to the next player
        """
        i = game.players.index(game.current_player)

        # Current player now waiting for their next turn
        game.current_player.wait()

        # Find the index of the next player
        try:
            game.current_player = game.players[i + 1]
        except IndexError:
            game.current_player = game.players[0]

        self._valid_moves = None

        game.current_player.start()

    def points_for_player(self, player):
        return game.components.played_components_for_player(player).player_points

    def show_state(self):
        # TODO: Remove this - for development only
        print(", ".join(["%s: %s" % (player.name, player.state)
                         for player in game.players]))

    # @property
    # def earned_multiple_tiles(self):
    #     return len(self.earned_tiles) > 1
    #
    # @property
    # def earned_single_tile(self):
    #     return len(self.earned_tiles) == 1
    #
    # @property
    # def earned_tiles(self):
    #     return []
    #

    @property
    def is_turn_complete(self):
        return game.mechanics.turn_complete(game.current_player)

    def init_components(self, component_collection_factory):
        player_count = len(game.players)

        components = component_collection_factory('card', raw_card_data)

        tiles = component_collection_factory('tile', raw_tile_data)
        shuffle(tiles)
        tiles = tiles[:player_count + 1]
        for i, tile in enumerate(tiles):
            tile.column = i
        components += tiles

        components += \
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
        shuffle(components)
        game.components.components = components
        self.draw_cards()

    @staticmethod
    def draw_card_for_row(row, column):
        card_deck = game.components.filter(
            state=ComponentStates.in_supply,
            component_class=Card,
            card_face_up=False,
            card_row=row)
        if card_deck:
            card = card_deck.components[0]
            card.face_up = True
            card.column = column

    def draw_cards(self):
        card_grid = game.components.table_card_grid
        for row in range(3):
            for j in range(4):
                if card_grid.card_grid[row][j] is None:
                    self.draw_card_for_row(row, j)

    def valid_moves(self, current_player):
        if not self._valid_moves:
            self._valid_moves = self.get_valid_moves(current_player)
        return self._valid_moves

    @staticmethod
    def get_valid_moves(current_player):
        """
        list of Move objects, each containing the pieces which the current
        player could take/buy/reserve
        """
        result = []

        # 3 different chips, if available
        top_table_chips = [c for c in game.components.top_table_chips if
                           c.chip_type != ChipType.yellow_gold]
        if len(top_table_chips) >= 3:
            result += [Move(pieces=list(c),
                            move_type=MoveType.take_different_chips)
                       for c in combinations(top_table_chips, 3)]

        # 2 different chips, if 2 available but not 3
        elif len(top_table_chips) == 2:
            result.append(Move(pieces=top_table_chips,
                               move_type=MoveType.take_different_chips))

        # 1 single chip,
        # if chips of only 1 type available and less than 4 of that type
        elif len(top_table_chips) == 1 and len(
                game.components.chips_from_supply(top_table_chips[0])) < 4:
            result.append(Move(pieces=top_table_chips,
                               move_type=MoveType.take_different_chips))

        for chip_type, chip_count in game.components.table_chips.items():
            if chip_type != ChipType.yellow_gold and chip_count >= 3:
                result.append(Move(
                    pieces=game.components.chips_from_supply(chip_type)[:2],
                    move_type=MoveType.take_same_chips
                ))

        # Buy a card from the supply
        result += [Move(pieces=[card], move_type=MoveType.buy_card)
                   for card in game.components.table_open_cards
                   if game.components.filter(
                state=ComponentStates.in_player_area,
                player=current_player
            ).count_by_colour().covers_cost(card.chip_cost)]

        # Buy a reserved card
        result += [Move(pieces=[card], move_type=MoveType.buy_card)
                   for card in
                   game.components.reserved_for_player(game.current_player)
                   if game.components.filter(
                state=ComponentStates.in_player_area,
                player=current_player
            ).count_by_colour().covers_cost(card.chip_cost)]

        # Reserve a card
        # If less than 3 cards reserved, and at least one yellow chip
        # available, can reserve any of the open cards
        if len(game.current_player.components.filter(
                component_class=Card, state=ComponentStates.in_reserved_area
        )) < 3 and ChipType.yellow_gold in game.components.table_chips:

            chip = game.components.chip_from_supply(ChipType.yellow_gold)
            result += [Move(
                pieces=[card, chip],
                move_type=MoveType.reserve_card,
                required=[chip]
            ) for card in game.components.table_open_cards]

        return result

    def valid_pieces(self, current_player):
        # Tile in holding area
        if game.current_player.state == PlayerStates.tile_selected:
            return set(game.components.holding_area_tiles)

        # Available tiles
        if game.current_player.state == PlayerStates.tiles_offered:
            return set(self.tiles_earned)

        # Main body of turn - pick any valid game piece
        valid_moves = self.valid_moves(current_player)
        pieces_taken = game.components.filter(
            state=ComponentStates.in_holding_area)

        result = set()
        for valid_move in valid_moves:
            main_split = SplitIntoIncludedAndExcluded(valid_move.pieces, pieces_taken)

            if main_split.excluded:
                # Some/all of the pieces taken are not in this move, so can't make this move
                continue

            if valid_move.required:
                required_split = SplitIntoIncludedAndExcluded(valid_move.required, pieces_taken)

                # No non-required pieces have been taken and not all required pieces have been taken
                if not required_split.excluded and required_split.remaining:
                    for piece in required_split.remaining:
                        result.add(piece)
                    continue

                # One or more non-required pieces taken and not all required pieces taken
                if required_split.excluded and required_split.remaining:
                   continue

            # Either no required pieces or all required pieces already taken. So can take the remaining pieces
            # from this move
            for piece in main_split.remaining:
                result.add(piece)

        return result

    def is_valid_action(self, current_player, component):
        valid_pieces = self.valid_pieces(current_player)
        if component in valid_pieces:
            return True

        # When taking the second chip of the same colour,
        # the piece in valid_pieces
        # is actually the one which is now in the holding area
        # So just check whether it is the same type

        if isinstance(component, Chip) \
                and any(c.chip_type == component.chip_type
                        for c in valid_pieces if isinstance(c, Chip)):
            return True

        return False

    def turn_complete(self, current_player):
        return len(self.valid_pieces(current_player)) == 0

    @staticmethod
    def pay_chip_cost(chip_cost, player):
        player_chips = game.components.filter(
            state=ComponentStates.in_player_area,
            component_class=Chip, player=player)
        card_rewards = game.components.filter(
            state=ComponentStates.in_player_area,
            component_class=Card, player=player). \
            count_by_colour()

        yellow_needed = 0
        for chip_type in chip_cost:
            chips_needed = chip_cost.colour_count[chip_type]
            if chip_type in card_rewards:
                chips_needed -= card_rewards.colour_count[
                    chip_type]

            chips = player_chips.filter(chip_type=chip_type)
            for i in range(chips_needed):
                if i < len(chips):
                    chips.components[i].to_supply()
                else:
                    yellow_needed += 1

        yellow_chips = player_chips.filter(chip_type=ChipType.yellow_gold)
        for i in range(yellow_needed):
            yellow_chips.components[i].to_supply()

    @property
    def tiles_earned(self):
        return [
            tile for tile in game.components.table_tiles
            if game.components.card_reward_for_player_including_pending(
                game.current_player
            ).covers_cost(tile.chip_cost)
            ]

    @property
    def earned_multiple_tiles(self):
        return len(self.tiles_earned) > 2

    @property
    def earned_single_tile(self):
        return len(self.tiles_earned) == 1

    def player_selects_single_tile(self):
        tile = self.tiles_earned[0]
        tile.to_holding_area()

    @property
    def final_round(self):
        return any(player.points >= 15 for player in game.players)
