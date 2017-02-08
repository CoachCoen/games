import pygame

from enum import Enum

from data import JewelType
from settings import config


class ColourPalette(Enum):
    table_cloth = 11
    corners = 12
    card_background = 13


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


def draw_text(location, text, font_size=24):
    myfont = pygame.font.SysFont("monospace",
                                 font_size * config.scaling_factor)

    label = myfont.render(text, 3, (255, 255, 0))

    location = _scale_vertices(location)
    easel.surface.blit(label, location)


def draw_circle(location, radius, colour):
    location = _scale_vertices(location)
    pygame.draw.circle(easel.surface, easel.colour(colour), location, radius)


class Easel(object):
    colour_palette = {
        ColourPalette.table_cloth: pygame.Color(20, 50, 20, 255),
        ColourPalette.corners: pygame.Color(70, 180, 70, 255),
        ColourPalette.card_background: pygame.Color(20, 20, 50, 255),
        JewelType.green_emerald.value: pygame.Color(0, 127, 0, 255),
        JewelType.red_ruby.value: pygame.Color(127, 0, 0, 255),
        JewelType.black_onyx.value: pygame.Color(10, 10, 10, 255),
        JewelType.white_diamond.value: pygame.Color(255, 255, 255, 255),
        JewelType.yellow_gold.value: pygame.Color(244, 238, 66, 255),
        JewelType.blue_sapphire.value: pygame.Color(0, 0, 127, 255),
    }

    def __init__(self):
        self.surface = None

    def init_easel(self, surface):
        self.surface = surface

    def colour(self, name):
        return self.colour_palette[name]

easel = Easel()
