import pygame

from enum import Enum

# from data import JewelType
from settings import config


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


def _scale_vertices(vertices):
    """
    Recursive scaling
    :param vertices:
    :return:
    """
    if isinstance(vertices, (int, float)):
        return config.scaling_factor * vertices
    return [_scale_vertices(i) for i in vertices]


def draw_pologon(vertices, colour):
    vertices = _scale_vertices(vertices)
    pygame.draw.polygon(easel.surface, easel.colour(colour),
                        vertices, 0)


def draw_rectangle(rectangle, colour):
    rectangle = _scale_vertices(rectangle)
    pygame.draw.rect(easel.surface, easel.colour(colour),
                     rectangle)


def draw_text(location, text, font_size=24, text_colour=None,
              reverse_colour=False):
    myfont = pygame.font.SysFont("monospace",
                                 int(font_size * config.scaling_factor))

    text_colour = easel.colour(text_colour) if text_colour \
        else (255, 255, 0, 255)

    if reverse_colour:
        text_colour = [(i + 127) % 256 for i in text_colour[:3]] + [255]

    label = myfont.render(text, 3, text_colour)

    location = _scale_vertices(location)
    easel.surface.blit(label, location)


def draw_circle(location, radius, colour):
    location = _scale_vertices(location)
    pygame.draw.circle(easel.surface, easel.colour(colour), location,
                       radius * config.scaling_factor)


class Easel(object):
    colour_palette = {
        ColourPalette.table_cloth: pygame.Color(20, 50, 20, 255),
        ColourPalette.corners: pygame.Color(70, 180, 70, 255),
        ColourPalette.card_background: pygame.Color(60, 60, 100, 255),
        ColourPalette.card_deck_background: pygame.Color(10, 70, 10, 255),
        ColourPalette.green_chip: pygame.Color(0, 127, 0, 255),
        ColourPalette.red_chip: pygame.Color(127, 0, 0, 255),
        ColourPalette.black_chip: pygame.Color(10, 10, 10, 255),
        ColourPalette.white_chip: pygame.Color(255, 255, 255, 255),
        ColourPalette.yellow_chip: pygame.Color(244, 238, 66, 255),
        ColourPalette.blue_chip: pygame.Color(0, 0, 127, 255),
    }

    def __init__(self):
        self.surface = None

    def init_easel(self, surface):
        self.surface = surface

    def colour(self, name):
        return self.colour_palette[name]

easel = Easel()
