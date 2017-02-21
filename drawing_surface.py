import pygame

from enum import Enum

from settings import config, Vector
from data import ChipType


class ColourPalette(Enum):
    table_cloth = 11
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

chip_type_to_colour = {
    ChipType.red_ruby: ColourPalette.red_chip,
    ChipType.blue_sapphire: ColourPalette.blue_chip,
    ChipType.white_diamond: ColourPalette.white_chip,
    ChipType.green_emerald: ColourPalette.green_chip,
    ChipType.black_onyx: ColourPalette.black_chip,
    ChipType.yellow_gold: ColourPalette.yellow_chip
}

def _translate_to_player(player_order, location):
    left = 0 if player_order in [0, 3] \
        else config.tabletop_size.x - config.player_area_size.x
    top = 0 if player_order in [0, 1] \
        else config.tabletop_size.y - config.player_area_size.y

    # TODO Tidy this up?
    if isinstance(location, Vector):
        return location + Vector(left, top)

    return (location[0] + left, location[1] + top) + tuple(location[2:])


def scale_vertices(vertices):
    """
    Recursive scaling
    :param vertices:
    :return:
    """
    if isinstance(vertices, (int, float)):
        return config.scaling_factor * vertices
    return [scale_vertices(i) for i in vertices]


def grow_rectangle(rectangle, increase):
    return (
        rectangle[0] - increase,
        rectangle[1] - increase,
        rectangle[2] + 2 * increase,
        rectangle[3] + 2 * increase
    )

def draw_pologon(vertices, colour):
    vertices = scale_vertices(vertices)
    pygame.draw.polygon(easel.surface, easel.colour(colour),
                        vertices, 0)


def draw_rectangle(rectangle, colour, player_order = None):
    if player_order:
        rectangle = _translate_to_player(
            player_order=player_order, location=rectangle
        )

    rectangle = scale_vertices(rectangle)
    pygame.draw.rect(easel.surface, easel.colour(colour),
                     rectangle)


def draw_text(location, text, font_size=24, text_colour=None,
              reverse_colour=False, player_order = None):
    myfont = pygame.font.SysFont("monospace bold",
                                 int(font_size * config.scaling_factor))

    text_colour = easel.colour(text_colour) if text_colour \
        else (255, 255, 0, 255)

    if reverse_colour:
        text_colour = [(i + 127) % 256 for i in text_colour[:3]] + [255]

    label = myfont.render(text, 3, text_colour)

    if player_order:
        location = _translate_to_player(
            player_order=player_order, location=location
        )

    location = scale_vertices(location)
    easel.surface.blit(label, location)


def draw_circle(location, radius, colour, player_order=None):
    if player_order:
        location = _translate_to_player(
            player_order=player_order, location=location
        )
    location = scale_vertices(location)
    pygame.draw.circle(easel.surface, easel.colour(colour), location,
                       int(radius * config.scaling_factor))


class Easel(object):
    colour_palette = {
        ColourPalette.table_cloth: pygame.Color(20, 50, 20, 255),
        ColourPalette.corners: pygame.Color(70, 180, 70, 255),
        ColourPalette.card_background: pygame.Color(60, 60, 100, 255),
        ColourPalette.card_deck_background: pygame.Color(10, 70, 10, 255),
        ColourPalette.player_area: pygame.Color(70, 70, 70, 70),
        ColourPalette.active_player_area: pygame.Color(100, 30, 30, 70),
        ColourPalette.holding_area: pygame.Color(120, 120, 120, 120),
        ColourPalette.green_chip: pygame.Color(0, 127, 0, 255),
        ColourPalette.red_chip: pygame.Color(127, 0, 0, 255),
        ColourPalette.black_chip: pygame.Color(10, 10, 10, 255),
        ColourPalette.white_chip: pygame.Color(255, 255, 255, 255),
        ColourPalette.yellow_chip: pygame.Color(244, 238, 66, 255),
        ColourPalette.blue_chip: pygame.Color(0, 0, 127, 255),
        ColourPalette.button: pygame.Color(120, 170, 170, 120)
    }

    def __init__(self):
        self.surface = None

    def init_easel(self, surface):
        self.surface = surface

    def colour(self, name):
        return self.colour_palette[name]

easel = Easel()
