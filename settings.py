# TODO Better variable name - top row?, top row left, top row right?
class Config(object):
    tabletop_width = 1366
    tabletop_height = 768

    scaling_factor = 2

    card_width = 100
    card_height = 120
    card_spacing = 10

    column_width = card_width + card_spacing
    row_height = card_height + card_spacing

    points_location_x = 40
    points_location_y = 10

    cost_location_x = 20
    cost_location_y = 15

    card_decks_location_x = 50
    card_decks_location_y = 120

    chip_size = 23
    chip_spacing = 10

    central_area_x = 360
    central_area_y = 130

    chip_stack_x = 0
    chip_stack_y = 100

    chip_stack_size = 25
    chip_stack_spacing = 5

    chip_cost_scaling = 0.5

    tile_size = 100
    tile_spacing = 10

    tiles_row_x = 50
    tiles_row_y = 0

    chip_font_size = 36

    reward_chip_x = 80
    reward_chip_y = 20
    reward_chip_scaling = 0.7

config = Config()
