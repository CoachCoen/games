import pygame

from enum import Enum

SCALING_FACTOR = 2


class Colour(Enum):
    table_cloth = 1
    corners = 2


def _scale_vertices(vertices):
    if isinstance(vertices, (int, float)):
        return SCALING_FACTOR * vertices
    return [_scale_vertices(i) for i in vertices]


def _draw_pologon(vertices, colour):
    vertices = _scale_vertices(vertices)
    pygame.draw.polygon(easel.surface, easel.colour(colour),
                        vertices, 0)


def _draw_rectangle(rectangle, colour):
    rectangle = _scale_vertices(rectangle)
    pygame.draw.rect(easel.surface, easel.colour(colour),
                     rectangle)


class Table(object):
    def _draw_tablecloth(self):
        _draw_rectangle((0, 0, easel.width, easel.height), Colour.table_cloth)

    def _draw_corners(self):
        for (x, y) in [
            (0, 0),
            (0, easel.height),
            (easel.width, easel.height),
            (easel.width, 0)
        ]:
            _draw_pologon([
                (x, abs(y - easel.height / 2.2)),
                (abs(x - easel.width / 2.2), y),
                (x, y)],
                Colour.corners
            )

    def draw(self):
        self._draw_tablecloth()
        self._draw_corners()


class Chip(object):
    def __init__(self, location, colour):
        self.location = location
        self.colour = colour

    def draw(self):
        pygame.draw.circle(easel.surface, easel.colour(self.colour),
                           self.location, 10)

class ChipStack(object):
    # TODO Coen: create an AbstractStack class?
    def __init__(self, location, colour, number):
        self.location = location
        self.colour = colour
        # TODO Coen: replace the number by a collection of Chips
        self.number = number

    def draw(self):
        pygame.draw.circle(easel.surface, easel.colour(self.colour),
                           self.location, 10)
        # TODO Coen: draw the number


class Easel(object):
    _colour_palette = {
        Colour.table_cloth: pygame.Color(20, 50, 20, 255),
        Colour.corners: pygame.Color(70, 180, 70, 255)
    }

    def __init__(self):
        self.width = None
        self.height = None
        self.surface = None

    def init_easel(self, surface, width, height):
        self.width = width
        self.height = height
        self.surface = surface

    def colour(self, name):
        return self._colour_palette[name]

easel = Easel()
