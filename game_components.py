"""
Classes for the game components: cards, chips and tiles. Components use
a state machines to track where they are
"""


from transitions import Machine

from embody import EmbodyTileMixin, EmbodyChipMixin, EmbodyCardMixin
from util_classes import ComponentStates


class AbstractGameComponent:
    """
    Abstract game component, sets up the state machine
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
            source=[ComponentStates.in_supply,
                    ComponentStates.in_reserved_area,
                    ComponentStates.in_player_area],
            dest=ComponentStates.in_holding_area,
            before='stash_state',
        ),

        # From holding area to player's hand
        dict(
            trigger='to_player_area',
            source=[ComponentStates.in_holding_area],
            dest=ComponentStates.in_player_area,
            before='stash_state',
        ),

        # From holding area to player's reserved area
        dict(
            trigger='to_reserved_area',
            source=[ComponentStates.in_holding_area],
            dest=ComponentStates.in_reserved_area,
            before='stash_state',
        ),

        # From player's hand back to the supply (e.g. when paying for a card)
        dict(
            trigger='to_supply',
            source=[ComponentStates.in_player_area,
                    ComponentStates.in_holding_area],
            dest=ComponentStates.in_supply,
            before='stash_state',
        )
    ]

    def __init__(self):
        """
        Initialises a component instance
        """

        self.previous_state = None
        self.player = None
        self.name = None
        self.points = 0

        self.machine = Machine(
            model=self,
            states=AbstractGameComponent.states,
            transitions=AbstractGameComponent.transitions,
            initial=ComponentStates.in_supply
        )

    def stash_state(self):
        """
        Remember the previous state, in case the current move gets cancelled
        """
        self.previous_state = self.state

    def move_back(self):
        """
        Move got cancelled, move the piece back
        """
        self.state = self.previous_state


class Card(AbstractGameComponent, EmbodyCardMixin):
    """
    A card, which consists of:

    * chip cost: a set of chips to be paid when buying this card
    * reward chip: the discount which this card gives towards
        buying another card
    * points: victory points
    """

    def __init__(self, chip_cost, chip_type, points, row):
        """
        Initialise the Card instance

        :param chip_cost: Cost of this card; how many chips and of what type
        :type chip_cost: colour_count.ChipCost
        :param chip_type: The 'reward' given by this card
        :type chip_type: ChipType
        :param int points: Number of victory points
        :param int row: If in the supply, the row for this card
        """
        super().__init__()
        self.chip_cost = chip_cost
        self.points = points
        self.chip_type = chip_type

        # 0 index the row
        self.row = row - 1

        self.column = None
        self.face_up = False


class Chip(AbstractGameComponent, EmbodyChipMixin):
    """
    A single chip
    """
    def __init__(self, chip_type):
        """
        Initialise the Chip instance

        :param chip_type: The type (colour) of chip
        :type chip_type: ChipType
        """
        super().__init__()
        self.chip_type = chip_type

    def __repr__(self):
        return repr(self.chip_type)


class Tile(AbstractGameComponent, EmbodyTileMixin):
    """
    A single nobles tile
    """
    def __init__(self, chip_cost, points):
        """
        Initialise the Tile instance

        :param chip_cost: Cost of this card; how many chips and of what type
        :type chip_cost: colour_count.ChipCost
        :param int points: Number of victory points
        """
        super().__init__()
        self.chip_cost = chip_cost
        self.points = points
        self.column = None
        self.player = None
