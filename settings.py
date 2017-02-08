class Config(object):
    tabletop_width = 1366
    tabletop_height = 768

    scaling_factor = 2

    card_width = 100
    card_height = 140
    card_spacing = 20

    column_width = card_width + card_spacing
    row_height = card_height + card_spacing

    points_location_x = 20
    points_location_y = 10

    cost_location_x = 20
    cost_location_y = 50

    chip_size = 20
    chip_spacing = 5

    central_area_x = 340
    central_area_y = 150

    chip_stack_x = 0
    chip_stack_y = 100

    chip_stack_size = 50
    chip_stack_spacing = 5

config = Config()
