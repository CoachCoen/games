import unittest
from unittest import mock

from app import game, init_game
from game_actions import MoveComponentToHoldingArea, ReturnCard, ReturnChip
from game_mechanics import Game
from game_components import ComponentFactory
from ai_simple import RandomAI


class TestGameActions(unittest.TestCase):

    @mock.patch.object(Game, 'refresh_display')
    def setUp(self, _):
        init_game(
            player_details=[
                ('Caroline', RandomAI()),
                ('Nigel', RandomAI()),
                ('Issie', RandomAI()),
                ('Coen', RandomAI())
            ]
        )
        game.current_player = game.players[0]
        game.current_player.start()
        self.component_factory = ComponentFactory()

    def test_take_card_from_grid(self):
        card = game.table.card_grid.cards[1][1]
        action = MoveComponentToHoldingArea(card)
        action.activate()

        # Card now in the holding area, no longer on the table
        self.assertEqual(game.holding_area.card, card)
        self.assertIsNone(game.table.card_grid.cards[1][1])

    def test_take_reserved_card(self):
        card = self.component_factory('card', '1 red:blue')
        game.current_player.reserved.empty()
        game.current_player.reserved.add(card)
        game.holding_area.card = None
        action = MoveComponentToHoldingArea(card)
        action.activate()

        # Card now in holding area, no longer reserved
        self.assertEqual(game.holding_area.card, card)
        self.assertFalse(game.current_player.reserved.contains(card))

    def test_return_card(self):
        card = game.table.card_grid.cards[1][1]
        card.take_card()
        action = MoveComponentToHoldingArea(card)
        action.activate()

        action = ReturnCard(card)
        action.activate()

        # Card back in grid, no longer in holding area
        self.assertEqual(game.table.card_grid.cards[1][1], card)
        self.assertIsNone(game.holding_area.card)

    def test_take_chip(self):
        chip = game.table.chips.chips[0]
        # action = TakeChip(chip)
        # action.activate()
        chip.move_to_holding_area()

        # Chip in holding area, not in the supply
        self.assertTrue(game.holding_area.chips.contains(chip))
        self.assertFalse(game.table.chips.contains(chip))

    def test_return_chip(self):
        chip = game.table.chips.chips[0]
        action = MoveComponentToHoldingArea(chip)
        action.activate()

        action = ReturnChip(chip)
        action.activate()

        # Chip in supply, not in the holding area
        self.assertTrue(game.table.chips.contains(chip))
        self.assertFalse(game.holding_area.chips.contains(chip))
