"""
What's the protocol:
Attach to a player
Player can either be AI or human
If AI, then player has an AI property, otherwise AI is set to None

Flow
    * At the start of a player's turn, if the player has an AI
        * Create list of possible moves
            * What will be gained
        * Pass list plus current game state to AI
        * AI chooses the move, execute the moves action(s)
            * action.activate(current_player)
            * Moves get shown in the holding area, as usual
        * Normal game flow continues
            * Human player then confirms the move
            * Or I can manually change the move
"""
from random import choice, shuffle
from game import game
from game_move import MoveType


class AbstractAI:
    """
    Abstract class for all AIs
    """

    def take_turn(self):
        """
        Choose a move and execute it
        """
        my_move = self._choose_move()
        if not my_move:
            return

        for item in my_move.pieces:
            item.to_holding_area()

    def _choose_move(self):
        """
        From game.mechanics.valid_moves(game.current_player),
        select a move (set of pieces to take)
        :return: the move
        """
        raise NotImplemented

    def select_tile(self):
        """
        From game.mechanics.tiles_earned, select the tile to claim
        :return: the tile to claim
        """
        self._tile_to_take.to_holding_area()

    @property
    def _tile_to_take(self):
        raise NotImplemented

    def select_chips_to_return(self):
        """
        Called when the current player has too many chips ( >10 )
        From game.components.chips_for_player(game.current_player),
        select the chip(s) to return
        :return: The chip(s) to return
        """
        for chip in self._chips_to_return:
            chip.to_holding_area()

    @property
    def _chips_to_return(self):
        raise NotImplemented


class RandomAI(AbstractAI):
    """
    Very simple AI - almost random
    """

    @staticmethod
    def _choose_move():
        """
        if possible, buy a card
        else, if possible, take 3 different chips
        else, if possible, take 2 same coloured chips
        else, reserve a card
        :return: the selected piece(s)
        """
        valid_moves = game.mechanics.valid_moves()
        valid_moves_idx = {move_type: [
            move for move in valid_moves if move.move_type == move_type
            ] for move_type in MoveType}

        for move_type in [
            MoveType.buy_card,
            MoveType.take_different_chips,
            MoveType.take_same_chips,
            MoveType.reserve_card
        ]:
            if len(valid_moves_idx[move_type]):
                return choice(valid_moves_idx[move_type])

        return None

    @property
    def _tile_to_take(self):
        """
        Pick a random tile to return
        """
        return choice(game.mechanics.tiles_earned)

    @property
    def _chips_to_return(self):
        """
        Pick a random set of chips, to bring the total number
        of chips for this player down to 10
        """
        chips = game.components.chips_for_player(
            game.current_player
        ).components[:]
        shuffle(chips)

        number_to_return = game.current_player.chip_count() - 10
        return chips[:number_to_return]
