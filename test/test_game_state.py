import unittest

from game_state import game
from game import init_game


class TestInitialGameState(unittest.TestCase):

    def setUp(self):
        init_game(
            player_details=[
                ('Caroline', None),
                ('Nigel', None),
                ('Issie', None),
                ('Coen', None)
            ]
        )

    # @unittest.skip('To be completed')
    def test_initial_cards(self):
        for expected, actual in zip([40, 30, 20], [len(deck) for deck in game.table.card_decks]):
            self.assertEqual(expected - 4, actual)

    @unittest.skip('To be completed')
    def test_costs_balanced(self):
        cost_count = {}
        for jewel_type in [i for i in JewelType if i != JewelType.yellow_gold]:
            cost_count[jewel_type] = sum(
                [c.cost.count(jewel_type) for c in self.gs.cards]
            )

        for jewel_type in [i for i in JewelType if i != JewelType.yellow_gold]:
            self.assertEqual(
                cost_count[jewel_type], cost_count[JewelType.red_ruby]
            )

    @unittest.skip('To be completed')
    def test_rewards_balanced(self):
        reward_count = {}
        for jewel_type in [i for i in JewelType if i != JewelType.yellow_gold]:
            reward_count[jewel_type] = sum(
                1 for c in self.gs.cards if c.jewel_type == jewel_type
            )

        for jewel_type in [i for i in JewelType if i != JewelType.yellow_gold]:
            self.assertEqual(
                reward_count[jewel_type], reward_count[JewelType.red_ruby]
            )


class TestTurnComplete(unittest):
    """
    A turn is complete when any of the following is true:
    - 3 different chips reserved
    - 2 chips of same type reserved
    - Yellow chip plus 1 card reserved
    - 1 chip reserved and less than 3 chips of this colour remaining and no other (non-yellow) colours remaining
    - 2 chips of different type reserved and no other colours remaining
    - card reserved
    """



if __name__ == '__main__':
    unittest.main()
