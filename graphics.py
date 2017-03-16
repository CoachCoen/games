import pygame
from enum import Enum

from settings import config
from chip_types import ChipType
from vector import Vector


class ColourPalette(Enum):
    table_cloth = 11
    table_cloth_final_round = 25
    corners = 12
    card_background = 13
    card_deck_background = 14
    green_chip = 15
    red_chip = 16
    black_chip = 17
    white_chip = 18
    yellow_chip = 19
    blue_chip = 20
    player_area = 21
    holding_area = 22
    button = 23
    active_player_area = 24


def translate_to_player(player_order, location):
    left = 0 if player_order in [0, 3] \
        else config.tabletop_size.x - config.player_area_size.x
    top = 0 if player_order in [0, 1] \
        else config.tabletop_size.y - config.player_area_size.y

    if isinstance(location, Vector):
        return location + Vector(left, top)

    return (location[0] + left, location[1] + top) + tuple(location[2:])


def circle_location_to_rectangle(location, size):
    return (location.x - size, location.y - size,
            2 * size, 2 * size)


def scale_vertices(vertices):
    """
    Recursive scaling
    :param vertices:
    :return:
    """
    if isinstance(vertices, (int, float)):
        return int(config.scaling_factor * vertices)
    return [scale_vertices(i) for i in vertices]


def grow_rectangle(rectangle, increase):
    return (
        rectangle[0] - increase,
        rectangle[1] - increase,
        rectangle[2] + 2 * increase,
        rectangle[3] + 2 * increase
    )


def draw_card(location, player_order=None):
    if player_order:
        location = translate_to_player(
            player_order=player_order, location=location
        )

    location = scale_vertices(location)
    easel.surface.blit(easel.card_image, location)


def draw_polygon(vertices, colour):
    vertices = scale_vertices(vertices)
    pygame.draw.polygon(easel.surface, easel.colour(colour),
                        vertices, 0)


def draw_rectangle(rectangle, colour, player_order=None):
    if player_order:
        rectangle = translate_to_player(
            player_order=player_order, location=rectangle
        )

    rectangle = scale_vertices(rectangle)
    pygame.draw.rect(easel.surface, easel.colour(colour),
                     rectangle)


def draw_text(location, text, font_size=24.0, text_colour=None,
              reverse_colour=False, player_order=None):
    myfont = pygame.font.SysFont("monospace bold",
                                 int(font_size * config.scaling_factor))

    text_colour = easel.colour(text_colour) if text_colour \
        else (255, 255, 0, 255)

    if reverse_colour:
        text_colour = [(i + 127) % 256 for i in text_colour[:3]] + [255]

    label = myfont.render(text, 3, text_colour)

    if player_order:
        location = translate_to_player(
            player_order=player_order, location=location
        )

    location = scale_vertices(location)
    easel.surface.blit(label, location)


def draw_circle(location, radius, colour, player_order=None):
    if player_order:
        location = translate_to_player(
            player_order=player_order, location=location
        )
    location = scale_vertices(location)
    pygame.draw.circle(easel.surface, easel.colour(colour), location,
                       int(radius * config.scaling_factor))


def draw_squares_row(location, counts, player_order=None):
    for i, chip_type in enumerate(ChipType):
        if counts[chip_type]:
            item_location = \
                location + Vector((1.5 * i - 0.5) * config.player_item_size, 0)
            draw_rectangle(
                item_location.to_rectangle(
                    Vector(config.player_item_size, config.player_item_size
                           )
                ), colour=chip_type,
                player_order=player_order
            )

            draw_text(
                item_location + Vector(5, 1),
                str(counts[chip_type]),
                text_colour=chip_type,
                reverse_colour=True,
                font_size=config.chip_font_size * 0.7,
                player_order=player_order
            )


def draw_circles_row(location, counts, player_order=None):
    for i, chip_type in enumerate(ChipType):
        if counts[chip_type]:
            item_location = \
                location + Vector(1.5 * i * config.player_item_size, 0)

            draw_circle(
                item_location,
                config.player_item_size/2,
                colour=chip_type,
                player_order=player_order
            )

            draw_text(
                item_location - Vector(5, 8),
                str(counts[chip_type]),
                text_colour=chip_type,
                reverse_colour=True,
                font_size=config.chip_font_size * 0.7,
                player_order=player_order
            )


def _draw_tablecloth(is_final_round):
    colour = ColourPalette.table_cloth_final_round \
        if is_final_round \
        else ColourPalette.table_cloth

    draw_rectangle((0, 0) + tuple(config.tabletop_size),
                   colour)


def _draw_player_corners():
    for (x, y) in [
        (0, 0),
        (0, config.tabletop_size.y),
        (config.tabletop_size.x, config.tabletop_size.y),
        (config.tabletop_size.x, 0)
    ]:
        draw_polygon([
            (x, abs(y - config.tabletop_size.x / 2.2)),
            (abs(x - config.tabletop_size.y / 2.2), y),
            (x, y)],
            ColourPalette.corners
        )


def draw_table(is_final_round):
    _draw_tablecloth(is_final_round)
    _draw_player_corners()


class Easel:
    # TODO: Move this into settings module
    colour_palette = {
        ColourPalette.table_cloth: pygame.Color(20, 50, 20, 255),
        ColourPalette.table_cloth_final_round: pygame.Color(10, 70, 100, 255),
        ColourPalette.corners: pygame.Color(70, 180, 70, 255),
        ColourPalette.card_background: pygame.Color(60, 60, 100, 255),
        ColourPalette.card_deck_background: pygame.Color(10, 70, 10, 255),
        ColourPalette.player_area: pygame.Color(70, 70, 70, 70),
        ColourPalette.active_player_area: pygame.Color(100, 30, 30, 70),
        ColourPalette.holding_area: pygame.Color(120, 120, 120, 120),
        ColourPalette.button: pygame.Color(120, 170, 170, 120),
        ChipType.green_emerald: pygame.Color(0, 127, 0, 255),
        ChipType.red_ruby: pygame.Color(127, 0, 0, 255),
        ChipType.black_onyx: pygame.Color(10, 10, 10, 255),
        ChipType.white_diamond: pygame.Color(255, 255, 255, 255),
        ChipType.yellow_gold: pygame.Color(244, 238, 66, 255),
        ChipType.blue_sapphire: pygame.Color(0, 0, 127, 255),
    }

    def __init__(self):
        self.surface = None
        self._card_image = None

    def init_easel(self, surface):
        self.surface = surface

    def colour(self, name):
        return self.colour_palette[name]

    @property
    def card_image(self):
        if self._card_image is None:
            self._card_image = pygame.image.\
                load('resources/yellow_card.png'). \
                convert_alpha()
            self._card_image = pygame.transform.scale(
                self._card_image,
                list(config.card_size * config.scaling_factor)
            )
        return self._card_image


easel = Easel()
