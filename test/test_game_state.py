import unittest

from game_state import game
from game import init_game
from game_objects import ComponentCollectionFactory, ComponentFactory

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


class TestTurnComplete(unittest.TestCase):
    """
    A turn is complete when any of the following is true:
    - 3 different chips reserved
    - 2 chips of same type reserved
    - Yellow chip plus 1 card reserved
    - 1 chip reserved and less than 3 chips of this colour remaining and no other (non-yellow) colours remaining
    - 2 chips of different type reserved and no other colours remaining
    - card reserved
    """
    def setUp(self):
        init_game(
            player_details=[
                ('Caroline', None),
                ('Nigel', None),
                ('Issie', None),
                ('Coen', None)
            ]
        )
        self.collection_factory = ComponentCollectionFactory()
        self.component_factory = ComponentFactory()

    def test_three_different_chips_reserved(self):
        game.table.chips = self.collection_factory('chip', '3 red,3 blue,3 white')

        # 3 different chips in holding area - complete
        game.holding_area.chips = self.collection_factory('chip', '1 red,1 blue,1 white')
        game.refresh_state()
        self.assertTrue(game.is_turn_complete)

        # 2 different chips in holding area - incomplete
        game.holding_area.chips = self.collection_factory('chip', '1 blue,1 white')
        game.refresh_state()
        self.assertFalse(game.is_turn_complete)

        # 3 chips, but only 2 different in holding area - incomplete
        game.holding_area.chips = self.collection_factory('chip', '2 blue,1 white')
        game.refresh_state()
        self.assertFalse(game.is_turn_complete)

    def test_two_same_chips_reserved(self):
        game.table.chips = self.collection_factory('chip', '3 red,3 blue,3 white')

        # 2 same chips in holding area - complete
        game.holding_area.chips = self.collection_factory('chip', '2 red')
        game.refresh_state()
        self.assertTrue(game.is_turn_complete)

    def test_card_plus_gold_reserved(self):
        game.table.chips = self.collection_factory('chip', '3 red,3 blue,3 white')

        # Yellow chip plus 1 card reserved - complete
        game.holding_area.chips = self.collection_factory('chip', '1 yellow')
        game.holding_area.card = self.component_factory('card', '2 red,1 blue:green')
        game.refresh_state()
        self.assertTrue(game.is_turn_complete)

        # Yellow chip but no cards - not done yet
        game.holding_area.chips = self.collection_factory('chip', '1 yellow')
        game.holding_area.card = None
        game.refresh_state()
        self.assertFalse(game.is_turn_complete)

    def test_one_chip_no_others_reserved(self):
        # 1 chip reserved and less than 3 chips of this colour remaining and no other (non-yellow) colours remaining
        game.table.chips = self.collection_factory('chip', '2 red,1 yellow')
        game.holding_area.chips = self.collection_factory('chip', '1 red')
        game.refresh_state()
        self.assertTrue(game.is_turn_complete)

        # 1 chip reserved and 3/+ chips of this colour remaining - can still take something
        game.table.chips = self.collection_factory('chip', '3 red,1 yellow')
        game.refresh_state()
        self.assertFalse(game.is_turn_complete)

    def test_two_chips_no_others_reserved(self):
        # 2 chips of different type reserved and no other colours remaining
        game.table.chips = self.collection_factory('chip', '2 red,1 green,1 yellow')
        game.holding_area.chips = self.collection_factory('chip', '1 red,1 green')
        game.refresh_state()
        self.assertTrue(game.is_turn_complete)

        # 2 chips of different type reserved, and other colour(s) remaining - can still take something
        game.table.chips = self.collection_factory('chip', '2 red,1 green,1 black,1 yellow')
        game.holding_area.chips = self.collection_factory('chip', '1 red,1 green')
        game.refresh_state()
        self.assertFalse(game.is_turn_complete)

    def test_card_reserved(self):
        # card reserved
        game.holding_area.chips = []
        game.holding_area.card = self.component_factory('card', '2 red,1 blue:green')
        game.refresh_state()
        self.assertTrue(game.is_turn_complete)


class TestAvailableActionSets(unittest.TestCase):
    def setUp(self):
        init_game(
            player_details=[
                ('Caroline', None),
                ('Nigel', None),
                ('Issie', None),
                ('Coen', None)
            ]
        )
        game.players[0].start()
        self.collection_factory = ComponentCollectionFactory()
        self.component_factory = ComponentFactory()

    def test_three_different_chips(self):
        """
        If at least 3 different chips available, can have any subset of 3 of them
        """
        game.table.chips = self.collection_factory('chip', '1 red,1 green,1 yellow,1 black,1 blue')
        game.refresh_state()
        # 4 different sub sets expected
        self.assertEqual(len(game.valid_action_sets['3 chips']), 4)

        game.table.chips = self.collection_factory('chip', '2 red,3 green,1 yellow,1 black,1 white,1 blue')
        game.refresh_state()
        # 5*4/2 different sub sets expected
        self.assertEqual(len(game.valid_action_sets['3 chips']), 10)

    def test_below_three_different_chips(self):
        """
        If less than 3 different chips available, can have one of each of the remaining typ(s)
        """
        game.table.chips = self.collection_factory('chip', '1 red,1 green,1 yellow')
        game.refresh_state()
        # 1 set expected
        self.assertEqual(len(game.valid_action_sets['3 chips']), 1)
        # Containing 2 chips
        self.assertEqual(len(game.valid_action_sets['3 chips'][0]), 2)

        game.table.chips = self.collection_factory('chip', '1 red,1 yellow')
        game.refresh_state()
        # 1 set expected
        self.assertEqual(len(game.valid_action_sets['3 chips']), 1)
        # Containing 1 chip
        self.assertEqual(len(game.valid_action_sets['3 chips'][0]), 1)

    def test_two_same_chips(self):
        """
        If more than 3 chips available of same type, can take 2 of them
        """
        game.table.chips = self.collection_factory('chip', '4 red,3 green,1 yellow')
        game.refresh_state()
        # 1 set expected
        self.assertEqual(len(game.valid_action_sets['2 chips']), 1)
        # Containing 2 chips
        self.assertEqual(len(game.valid_action_sets['2 chips'][0]), 2)

        game.table.chips = self.collection_factory('chip', '4 red,4 green,1 yellow')
        game.refresh_state()
        # 2 sets expected
        self.assertEqual(len(game.valid_action_sets['2 chips']), 2)
        # Containing 2 chips
        self.assertEqual(len(game.valid_action_sets['2 chips'][0]), 2)

        game.table.chips = self.collection_factory('chip', '3 red,3 green,1 yellow')
        game.refresh_state()
        # No sets expected
        self.assertEqual(len(game.valid_action_sets['2 chips']), 0)

    def test_can_buy_reserved_cards(self):
        """
        If player has a card reserved, and can afford to buy it, is in valid_action_sets['reserved']
        """
        card = self.component_factory('card', '2 red,1 blue:green')
        game.current_player.reserved.empty()
        game.current_player.reserved.add(card)
        game.current_player.chips = self.collection_factory('chip', '2 red,1 blue')
        game.refresh_state()

        # 1 card expected
        self.assertEqual(len(game.valid_action_sets['buy reserved']), 1)
        self.assertIn(card, game.valid_action_sets['buy reserved'])


if __name__ == '__main__':
    unittest.main()
