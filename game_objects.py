"""
    Game objects: cards, chips, tokens
    Game object containers: card deck, card slot, card grid,
        chip collection, tile collection, table, holding area
"""
from transitions import Machine

from embody import EmbodyTileMixin
from states import PlayerStates, ComponentStates

from embody import EmbodyCardMixin


class AbstractGameComponent(object):
    """
    Abstract game component
    """
    states = [
        ComponentStates.in_supply,
        ComponentStates.in_holding_area,
        ComponentStates.in_reserved_area,
        ComponentStates.in_player_area
    ]

    transitions = [
        # Move component to holding area
        dict(
            trigger='to_holding_area',
            source=[ComponentStates.in_supply, ComponentStates.in_reserved_area],
            dest=ComponentStates.in_holding_area
        ),

        # From holding area to player's hand
        dict(
            trigger='to_player_area',
            source=[ComponentStates.in_holding_area],
            dest=ComponentStates.in_player_area,
        ),

        # From holding area to player's reserved area
        dict(
            trigger='to_reserved_area',
            source=[ComponentStates.in_holding_area],
            dest=ComponentStates.in_reserved_area,
        ),

        # From player's hand back to the supply (e.g. when paying for a card)
        dict(
            trigger='to_supply',
            source=[ComponentStates.in_player_area],
            dest=ComponentStates.in_supply
        )
    ]

    def __init__(self):
        self.previous_position = None
        self.player = None
        self.name = None

        self.machine = Machine(
            model=self,
            states=AbstractGameComponent.states,
            transitions=AbstractGameComponent.transitions,
            initial=ComponentStates.in_supply
        )


class Card(AbstractGameComponent, EmbodyCardMixin):
    """
    A card, which consists of:
    - chip cost: a set of chips to be paid when buying this card
    - reward chip: the discount which this card gives towards
        buying another card
    - points: victory points
    """
    def __init__(self, chip_cost, chip_type, points, row):
        super().__init__()
        self.chip_cost = chip_cost
        self.points = points
        self.chip_type = chip_type
        self.row = row - 1  # 0 index the row
        self.column = None
        self.face_up = False


class Chip(AbstractGameComponent):
    """
    Chip class
    """
    def __init__(self, chip_type):
        super().__init__()
        self.chip_type = chip_type

    def __repr__(self):
        return repr(self.chip_type)


class Tile(AbstractGameComponent, EmbodyTileMixin):
    def __init__(self, chip_cost, points):
        super().__init__()
        self.chip_cost = chip_cost
        self.points = points
        self.column = None
        self.player = None
