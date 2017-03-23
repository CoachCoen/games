from enum import Enum


class ChipType(Enum):
    """
    The different types of chips/jewels
    """
    green_emerald = 1
    blue_sapphire = 2
    red_ruby = 3
    white_diamond = 4
    black_onyx = 5
    yellow_gold = 6


class PlayerStates:
    player_waiting = 'waiting_for_turn'
    turn_started = 'turn_started'
    tiles_offered = 'tiles_offered'
    turn_finished = 'turn_finished'
    too_many_chips = 'too_many_chips'


class ComponentStates:
    in_supply = 'in_supply'
    in_holding_area = 'in_holding_area'
    in_reserved_area = 'reserved_by_player'
    in_player_area = 'in_player_area'
