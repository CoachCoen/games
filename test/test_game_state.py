import unittest

from game_state import GameState, JewelType

class TestInitialGameState(unittest.TestCase):

    def setUp(self):
        self.gs = GameState([1, 2, 3, 4])

    def test_initial_cards(self):
        cards = self.gs.cards
        # TODO: Check this is the righ number
        self.assertEqual(len(cards), 90)

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

if __name__ == '__main__':
    unittest.main()
