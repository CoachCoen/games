import unittest
from unittest.mock import patch
# import random

from ai_simple import RandomAI
from game import game
# from ai_simple import random


# remove random element from the random ai
def take_first(my_list):
    return my_list[0]


def dummy_action_sets():
    return {
        'card': 'Hello'
    }


@unittest.skip('Under development')
class TestAISimple(unittest.TestCase):

    # @patch(random, 'choice', take_first)
    @patch('random.choice', new_callable=take_first)
    # @patch('game.valid_action_sets', new_callable=dummy_action_sets)
    @patch.object(game, 'valid_action_sets', new_callable=dummy_action_sets)
    def test_random_ai(self, _1, _2):
        random_ai = RandomAI()
        move = random_ai._choose_move()
        self.assertEqual(move, 'Hello')

if __name__ == '__main__':
    unittest.main()
