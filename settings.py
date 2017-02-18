# TODO Move this to a more sensible place
class Vector(object):
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __iter__(self):
        yield self.x
        yield self.y

    def to_rectangle(self, size):
        return list(self) + list(size)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


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

    player_area_size = Vector(300, 180)

    player_name_location = Vector(5, 5)

    player_chip_stack_location = Vector(40, 55)

    player_points_location = Vector(player_area_size.x - 40, 20)

    holding_area_size = Vector(350, 200)
    holding_area_location = Vector(1000, 300)

config = Config()
