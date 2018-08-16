import unittest
from unittest.mock import patch, PropertyMock

import ai_simple
from game_mechanics import Game


def mock_choice(my_list):
    return my_list[0]


class TestAISimple(unittest.TestCase):
    """
    Test the simple AIs, which pick a move from a list of valid moves
    """

    @patch('ai_simple.choice', side_effect=mock_choice)
    @patch.object(Game, 'valid_action_sets', new_callable=PropertyMock)
    def test_random_ai(self, m_valid_action_sets, _):
        """
        Random AI picks a (near) random move from a list of possible moves
        """
        random_ai = ai_simple.RandomAI()

        m_valid_action_sets.return_value = {
            'card': ['Hello', 'Fred', 'Sue']
        }
        move = random_ai._choose_move()
        self.assertEqual(move, 'Hello')

        # Picks a card over a set of 3 chips
        m_valid_action_sets.return_value = {
            '3 chips': ['Green', 'Blue', 'White'],
            'card': ['Hello', 'Fred', 'Sue']
        }
        move = random_ai._choose_move()
        self.assertEqual(move, 'Hello')

        # Sanity check
        m_valid_action_sets.return_value = {
            '3 chips': ['Green', 'Blue', 'White'],
            'card': []
        }
        move = random_ai._choose_move()
        self.assertEqual(move, 'Green')

if __name__ == '__main__':
    unittest.main()
