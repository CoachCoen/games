import pygame

from vector import Vector


class Config(object):
    tabletop_size = Vector(1366, 768)
    scaling_factor = 2

    card_size = Vector(100, 120)
    card_spacing = 10

    column_width = card_size.x + card_spacing
    row_height = card_size.y + card_spacing

    points_location = Vector(40, 10)

    cost_location = Vector(20, 15)

    card_decks_location = Vector(50, 120)

    chip_size = 23
    chip_spacing = 10

    central_area_location = Vector(360, 130)

    chip_stack_location = Vector(0, 100)

    chip_stack_size = 25
    chip_stack_spacing = 5

    chip_cost_scaling = 0.5

    tile_size = Vector(100, 100)
    tile_spacing = 10

    tiles_row_location = Vector(50, 0)

    chip_font_size = 36

    reward_chip_location = Vector(80, 20)
    reward_chip_scaling = 0.7

    player_area_size = Vector(300, 225)

    player_name_location = Vector(5, 5)

    player_chip_stack_location = Vector(40, 40)
    player_item_size = 30
    player_card_deck_location = player_chip_stack_location + Vector(0, 20)
    player_reserved_location = Vector(10, 95)

    player_points_location = Vector(player_area_size.x - 30, 5)

    holding_area_size = Vector(350, 200)
    holding_area_location = Vector(1000, 300)

    holding_area_card_location = Vector(30, 30)
    holding_area_chips_location = Vector(150, 30)
    holding_area_name_location = Vector(5, 5)
    holding_area_chip_scaling = 1

    button_text_location = Vector(5, 5)
    # TODO: Dynamically determine button size
    button_size = Vector(80, 30)
    cancel_button_location = Vector(10, 160)
    confirm_button_location = Vector(100, 160)

config = Config()
