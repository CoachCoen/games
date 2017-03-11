"""
What's the protocol:
Attach to a player
Player can either be AI or human
If AI, then player has an AI property, otherwise AI is set to None

Flow
    * At the start of a player's turn, if the player has an AI
        * Create list of possible moves
            * What will be gained
            * What is the button's action for this move
                TakeChip(chip, holding_area)
                TakeCard(card, holding_area)
        * Pass list plus current game state to AI
        * AI chooses the move, execute the moves action(s)
            * action.activate(current_player)
            * Moves get shown in the holding area, as usual
        * Normal game flow continues
            * I then confirm the move, so I can see what happened
            * Or I could manually change the move
"""
from random import choice
from game import game
from game_move import MoveType


class AbstractAI:
    """
    Abstract class for all AIs
    """

    # TODO: Refactor so the AI returns the actions it's chosen, rather than actually execute them
    def take_turn(self):
        raise NotImplemented


class RandomAI(AbstractAI):
    @staticmethod
    def _choose_move():
        valid_moves = game.mechanics.valid_moves(game.current_player)
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

    def take_turn(self):
        my_move = self._choose_move()
        if not my_move:
            return

        for item in my_move.pieces:
            item.to_holding_area()

    def select_tile(self):
        tiles = game.mechanics.tiles_earned
        tile = choice(tiles)
        tile.to_holding_area()
