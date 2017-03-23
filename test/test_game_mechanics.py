import unittest
from unittest.mock import patch

from game_mechanics import GameMechanics
from game import game
from game_component_database import ComponentDatabase
from game_move import MoveType, Move
from game_components import Chip
from util_classes import ChipType
from states import ComponentStates


class TestValidPiece(unittest.TestCase):
    def setUp(self):
        self.game_mechanics = GameMechanics()
        game.components = ComponentDatabase()
        self.green_chip = Chip(chip_type=ChipType.green_emerald)
        self.blue_chip = Chip(chip_type=ChipType.blue_sapphire)
        self.red_chip = Chip(chip_type=ChipType.red_ruby)
        self.white_chip = Chip(chip_type=ChipType.white_diamond)
        self.black_chip = Chip(chip_type=ChipType.black_onyx)
        self.yellow_chip = Chip(chip_type=ChipType.yellow_gold)

    @patch('game_mechanics.GameMechanics.valid_moves')
    def test_nothing_taken_yet(self, mock_valid_moves):
        """
        If no pieces have been taken yet, can take any
        which is part of a valid move (as long as we don't specify
        any required pieces - that's in a different test)
        """

        # Sanity test
        self.assertEqual(self.game_mechanics.valid_pieces(None), set())

        # Nothing taken, so return all pieces in all moves
        mock_valid_moves.return_value = [
            Move(move_type=MoveType.take_different_chips, pieces=[self.green_chip]),
            Move(move_type=MoveType.take_different_chips, pieces=[self.blue_chip, self.white_chip])
        ]
        for chip in (self.white_chip, self.green_chip, self.blue_chip):
            self.assertIn(chip, self.game_mechanics.valid_pieces(None))

    @patch('game_mechanics.GameMechanics.valid_moves')
    def test_moves_not_in_progress(self, mock_valid_moves):
        """
        If one or more pieces have been taken, only moves which contain all these pieces should be allowed,
        so only return pieces from those moves
        """

        # Single piece taken, only return pieces in moves which include it, but not the piece itself
        mock_valid_moves.return_value = [
            Move(move_type=MoveType.take_different_chips, pieces=[self.green_chip]),
            Move(move_type=MoveType.take_different_chips, pieces=[self.blue_chip, self.white_chip]),
            Move(move_type=MoveType.take_different_chips, pieces=[self.blue_chip, self.black_chip])
        ]
        chip = Chip(chip_type=ChipType.blue_sapphire)
        chip.state = ComponentStates.in_holding_area
        game.components.components = [chip]
        for chip, included in (
                (self.white_chip, True),
                (self.green_chip, False),
                (self.red_chip, False),
                (self.black_chip, True),
                (self.blue_chip, False),
                (self.yellow_chip, False),
        ):
            if included:
                self.assertIn(chip, self.game_mechanics.valid_pieces(None))
            else:
                self.assertNotIn(chip, self.game_mechanics.valid_pieces(None))

        # Works fine for moves which include two of the same type
        mock_valid_moves.return_value = [
            Move(move_type=MoveType.take_different_chips, pieces=[self.green_chip]),
            Move(move_type=MoveType.take_same_chips, pieces=[self.blue_chip, self.blue_chip]),
            Move(move_type=MoveType.take_different_chips, pieces=[self.blue_chip, self.black_chip])
        ]
        chip = Chip(chip_type=ChipType.blue_sapphire)
        chip.state = ComponentStates.in_holding_area
        game.components.components = [chip]
        for chip, included in (
                (self.white_chip, False),
                (self.green_chip, False),
                (self.red_chip, False),
                (self.black_chip, True),
                (self.blue_chip, True),
                (self.yellow_chip, False),
        ):
            if included:
                self.assertIn(chip, self.game_mechanics.valid_pieces(None))
            else:
                self.assertNotIn(chip, self.game_mechanics.valid_pieces(None))

    @patch('game_mechanics.GameMechanics.valid_moves')
    def test_required_pieces(self, mock_valid_moves):
        """
        If a Move object contains one or more required pieces
            If all required pieces for that move are in the holding area, return any remaining pieces from that move
            If a required piece for that move is not in the holding area, return any required pieces
                from that move which are not in the holding area, but don't return any of the other pieces
        If a piece can be taken because of a different move, regardless of the status of any move with
            required piece(s), treat it as normal
        """
        mock_valid_moves.return_value = [
            Move(move_type=MoveType.take_different_chips, pieces=[self.green_chip]),
            Move(move_type=MoveType.take_same_chips, pieces=[self.blue_chip, self.red_chip], required=[self.red_chip]),
            Move(move_type=MoveType.take_different_chips, pieces=[self.black_chip])
        ]
        chip = Chip(chip_type=ChipType.blue_sapphire)
        chip.state = ComponentStates.in_holding_area
        game.components.components = []
        for chip, included in (
                (self.white_chip, False),
                (self.green_chip, True),
                (self.red_chip, True),
                (self.black_chip, True),
                (self.blue_chip, False),
                (self.yellow_chip, False),
        ):
            if included:
                self.assertIn(chip, self.game_mechanics.valid_pieces(None))
            else:
                self.assertNotIn(chip, self.game_mechanics.valid_pieces(None))

        # TODO: A few more tests here?

if __name__ == '__main__':
    unittest.main()
