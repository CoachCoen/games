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
# import random

from game_objects import Chip, Card
from game_actions import TakeChip, TakeCard
from game_state import game


class AbstractAI(object):
    def __init__(self):
        self.player = None


class RandomAI(AbstractAI):
    @staticmethod
    def _choose_move():
        valid_action_sets = game.valid_action_sets

        for action_type in ['card', '3 chips', '2 chips', 'reserve card', 'buy reserved']:
            if len(valid_action_sets[action_type]):
                return choice(valid_action_sets[action_type])

        return None

    @staticmethod
    def _action_for_item(item):
        for object_type, action in [
            (Chip, TakeChip),
            (Card, TakeCard)
        ]:
            if isinstance(item, object_type):
                return action(item)
        return None

    def take_turn(self):
        my_move = self._choose_move()
        if not my_move:
            return

        actions = [self._action_for_item(item) for item in my_move
                   if self._action_for_item(item)]

        for action in actions:
            action.activate()


class SimpleAI(AbstractAI):
    pass
