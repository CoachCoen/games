from enum import Enum


class ComponentState(Enum):
    """
    Different places where a component can be
    Used to decide what to do when clicking on a component
    """
    holding_area = 1
    player = 2
    card_grid = 3
    card_decks = 4
    reserved = 5
    table = 6
