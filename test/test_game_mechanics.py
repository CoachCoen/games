import unittest
from unittest.mock import patch

from game_mechanics import GameMechanics


class TestValidPiece(unittest.TestCase):
    def setUp(self):
        self.game_mechanics = GameMechanics()

    @patch('game_mechanics.GameMechanics.valid_moves')
    def test_nothing_taken_yet(self, mock_valid_moves):
        """
        If no pieces have been taken yet, can take any
        which is part of a valid move (as long as we don't specify
        any required pieces - that's in a different test)
        """
        mock_valid_moves.return_value = []
        self.assertEqual(self.game_mechanics.valid_pieces(None), [])

if __name__ == '__main__':
    unittest.main()
