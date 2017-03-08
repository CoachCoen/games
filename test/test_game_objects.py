import unittest

from game_components import ComponentCollectionFactory
from chip_types import ChipType


class TestGameObjects(unittest.TestCase):
    def test_component_collection_factory_chips(self):
        chips = ComponentCollectionFactory()('chip', '3 red,4 blue')
        for chip_count, chip_type in [
            (3, ChipType.red_ruby),
            (4, ChipType.blue_sapphire)
        ]:
            self.assertEqual(
                sum(1 for c in chips.chips if c.chip_type == chip_type),
                chip_count
            )

    def test_component_collection_factory_cards(self):
        cards = ComponentCollectionFactory()(
            'card',
            """5 red:red
            6 blue:green,1"""
        )

        self.assertEqual(len(cards.cards), 2)

        # Cards can be created in any order, so can't simply
        # loop through them and always expect same results
        # Instead compare the reward type
        for card in cards.cards:
            for (cost_type, cost_count, reward_type, points) in [
                    (ChipType.blue_sapphire, 6, ChipType.green_emerald, 1),
                    (ChipType.red_ruby, 5, ChipType.red_ruby, 0)
            ]:
                if card.reward_chip.chip_type == reward_type:
                    self.assertEqual(card.chip_cost.chips[0].chip_type, cost_type)
                    self.assertEqual(len(card.chip_cost.chips), cost_count)
                    self.assertEqual(card.points, points)

    # def test_component_collection_factory_tiles(self):
    #     tiles = ComponentCollectionFactory()(
    #         'tile',
    #
    #     )

if __name__ == '__main__':
    unittest.main()
