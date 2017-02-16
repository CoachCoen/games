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

    points_location_x = 20
    points_location_y = 10

    cost_location_x = 20
    cost_location_y = 45

    card_decks_location_x = 50
    card_decks_location_y = 50

    chip_size = 25
    chip_spacing = 10

    central_area_x = 340
    central_area_y = 130

    chip_stack_x = 0
    chip_stack_y = 100

    chip_stack_size = 25
    chip_stack_spacing = 5

    nobles_tile_size = 100
    nobles_tile_spacing = 10

    noble_tiles_row_x = 160
    noble_tiles_row_y = 0

config = Config()
