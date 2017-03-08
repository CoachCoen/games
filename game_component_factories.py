from utils import chip_type_for_colour_name
from colour_count import ChipCost
from game_components import Chip, Tile, Card


class AbstractFactory(object):
    """
    Simple grouping of factory classes
    """
    pass


class ComponentFactory(AbstractFactory):
    def __call__(self, component_type, details):
        func = {
            'chip': self.chip_factory,
            'card': self.card_factory,
            'tile': self.tile_factory
        }[component_type]
        return func(details)

    @staticmethod
    def chip_factory(details):
        return Chip(chip_type_for_colour_name(details))

    @staticmethod
    def card_factory(details):
        row, raw_cost, reward_text = details.split(':')
        row = int(row)

        if "," in reward_text:
            # e.g. 5 black, 3 red, 3 black, 3 white: 1 blue, 3 points
            raw_chip_type, raw_reward_points = reward_text.split(",")
            reward_points = int(raw_reward_points)
        else:
            raw_chip_type = reward_text
            reward_points = 0

        chip_type = chip_type_for_colour_name(raw_chip_type)

        chip_cost = ChipCost(raw_colour_count=raw_cost)

        return Card(
            chip_cost=chip_cost,
            chip_type=chip_type,
            points=reward_points,
            row=row
        )

    @staticmethod
    def tile_factory(details):
        raw_cost, raw_points = details.split(':')
        # component_collection_factory = ComponentCollectionFactory()
        # chip_cost = component_collection_factory('chip', raw_cost.strip())
        return Tile(chip_cost=ChipCost(raw_colour_count=raw_cost.strip()),
                    points=int(raw_points))


class ComponentCollectionFactory(AbstractFactory):
    def __init__(self):
        self.component_factory = ComponentFactory()

    def __call__(self, component_type, details):
        func = {
            'chip': self.chip_collection_factory,
            'card': self.card_collection_factory,
            'tile': self.tile_collection_factory
        }[component_type]
        return func(details)

    def chip_collection_factory(self, details):
        chips = []

        for stack_data in details.split(","):
            if stack_data:
                chip_count, colour_name = stack_data.strip().split(" ")
                chip_count = int(chip_count)
                for _ in range(chip_count):
                    chip = self.component_factory('chip', colour_name)
                    chips.append(chip)
        return chips

    def card_collection_factory(self, details):
        return [
            self.component_factory('card', card_details)
            for card_details in details.split('\n') if card_details
            ]

    def tile_collection_factory(self, details):
        return [
            self.component_factory('tile', details='%s:3' % raw_cost)
            for raw_cost in details.split("\n")
            if raw_cost.strip()
            ]
