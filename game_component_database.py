from chip_types import ChipType
from colour_count import ColourCount, ChipStacks, PlayerChipStack, \
    PlayerCardStack
from game_components import Chip, Card, Tile

from embody import EmbodyCardGridMixin, EmbodyCardDeckCountMixin, \
    EmbodyHoldingAreaMixin

from states import ComponentStates


class CardGrid(EmbodyCardGridMixin):
    """
    3 rows, 4 columns of 'open' cards on the table
    """
    def __init__(self, card_grid):
        self.card_grid = card_grid


class CardDeckCount(EmbodyCardDeckCountMixin):
    """
    The number of cards in the 3 card decks on the table
    """
    def __init__(self, card_deck_count):
        self.card_deck_count = card_deck_count


class AbstractComponentDatabase:

    def __init__(self, components=None):
        self.components = components if components is not None else []

    def __iter__(self):
        return iter(self.components)

    def __len__(self):
        return len(self.components)

    @property
    def is_empty(self):
        return len(self) == 0


class ComponentDatabase(AbstractComponentDatabase):

    ############################################################
    # Filter methods
    # by component state, class, (card) face up/down,
    # chip/reward type and/or player
    ############################################################
    def _filter_by_state(self, state):
        return ComponentDatabase(
            [c for c in self.components
             if c.state == state])

    def _filter_by_class(self, component_class):
        return ComponentDatabase(
            [c for c in self.components
             if isinstance(c, component_class)]
        )

    def _filter_by_card_face_up(self, card_face_up):
        return ComponentDatabase(
            [c for c in self.components
             if c.face_up == card_face_up]
        )

    def _filter_by_card_row(self, card_row):
        return ComponentDatabase(
            [c for c in self.components
             if c.row == card_row]
        )

    def _filter_by_chip_type(self, chip_type):
        return ComponentDatabase(
            [c for c in self.components
             if c.chip_type == chip_type]
        )

    def _filter_by_player(self, player):
        return ComponentDatabase(
            [c for c in self.components
             if c.state in [ComponentStates.in_player_area, ComponentStates.in_reserved_area] and
             c.player == player]
        )

    def filter(self, state=None, component_class=None, card_face_up=None,
               card_row=None, chip_type=None, player=None):
        result = self
        if state is not None:
            result = result._filter_by_state(state)
        if component_class is not None:
            result = result._filter_by_class(component_class)
        if card_face_up is not None:
            result = result._filter_by_card_face_up(card_face_up)
        if card_row is not None:
            result = result._filter_by_card_row(card_row)
        if chip_type is not None:
            result = result._filter_by_chip_type(chip_type)
        if player is not None:
            result = result._filter_by_player(player)
        return result

    ############################################################
    # Methods to group/summarise the data
    ############################################################
    def count_for_colour(self, chip_type):
        return sum(1 for c in self.components
                   if c.chip_type == chip_type)

    def count_by_colour(self, result_class=ColourCount):
        return result_class({
            chip_type: self.count_for_colour(chip_type)
            for chip_type in ChipType
        })

    def count_by_row(self):
        return CardDeckCount({
            i: sum(1 for c in self.components if c.row == i)
            for i in range(3)
        })

    def as_grid(self):
        """
        3 rows for 4 cells each
        """
        result = [[None] * 4, [None] * 4, [None] * 4]

        for c in self.components:
            result[c.row][c.column] = c

        return CardGrid(result)

    @property
    def player_points(self):
        return sum(c.points for c in self.components)

    ############################################################
    # Methods representing specific game 'elements'
    ############################################################
    def reserved_for_player(self, player):
        return self.filter(
            state=ComponentStates.in_reserved_area,
            component_class=Card,
            player=player
        )

    @property
    def table_card_grid(self):
        return self.filter(
            state=ComponentStates.in_supply,
            component_class=Card,
            card_face_up=True
        ).as_grid()

    @property
    def table_chips(self):
        # Chip stacks on the table
        return self.filter(
            state=ComponentStates.in_supply, component_class=Chip
        ).count_by_colour(ChipStacks).filter(remove_blanks=True)

    @property
    def top_table_chips(self):
        # Actual chips on top of each chip stack
        return [self.chip_from_supply(chip_type)
                for chip_type in self.table_chips]

    def chip_from_supply(self, chip_type):
        try:
            return self.chips_from_supply(chip_type)[0]
        except IndexError:
            return None

    def chips_from_supply(self, chip_type):
        return self.filter(
            state=ComponentStates.in_supply,
            component_class=Chip,
            chip_type=chip_type
        ).components

    def chip_count_for_player(self, player):
        return self.filter(
            state=ComponentStates.in_player_area,
            component_class=Chip,
            player=player
        ).count_by_colour(PlayerChipStack)

    def card_reward_for_player(self, player):
        return self.filter(
            state=ComponentStates.in_player_area,
            component_class=Card,
            player=player
        ).count_by_colour(PlayerCardStack)

    def card_reward_for_player_including_pending(self, player):
        cards = self.filter(
            state=ComponentStates.in_player_area,
            component_class=Card,
            player=player
        ).components + self.filter(
            state=ComponentStates.in_holding_area,
            component_class=Card
        ).components
        return ComponentDatabase(components=cards).count_by_colour()

    def reserved_cards_for_player(self, player):
        return self.filter(
            state=ComponentStates.in_reserved_area,
            component_class=Card,
            player=player
        )

    def played_components_for_player(self, player):
        return self.filter(
            state=ComponentStates.in_player_area,
            player=player
        )

    @property
    def table_card_stacks(self):
        return self.filter(
            state=ComponentStates.in_supply,
            component_class=Card,
            card_face_up=False
        ).count_by_row()

    @property
    def table_open_cards(self):
        return self.filter(
            state=ComponentStates.in_supply,
            component_class=Card,
            card_face_up=True
        )

    @property
    def holding_area_components(self):
        return self.filter(
            state=ComponentStates.in_holding_area
        )

    @property
    def holding_area_chips(self):
        return self.filter(
            state=ComponentStates.in_holding_area, component_class=Chip
        )

    @property
    def holding_area_tiles(self):
        return self.filter(
            state=ComponentStates.in_holding_area, component_class=Tile
        )

    @property
    def holding_area_cards(self):
        return self.filter(
            state=ComponentStates.in_holding_area, component_class=Card
        )

    @property
    def holding_area_tiles(self):
        return self.filter(
            state=ComponentStates.in_holding_area, component_class=Tile
        )

    @property
    def holding_area(self):
        """
        Filter out components in the holding area and return
        a HoldingArea instance, to give it the correct embody() method
        """
        return HoldingArea(self.filter(
            state=ComponentStates.in_holding_area
        ).components)

    @property
    def table_tiles(self):
        return self.filter(
            state=ComponentStates.in_supply, component_class=Tile
        )


class HoldingArea(ComponentDatabase, EmbodyHoldingAreaMixin):
    pass
