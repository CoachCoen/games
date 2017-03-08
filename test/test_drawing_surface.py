import unittest

from vector import Vector
from graphics import translate_to_player, scale_vertices, grow_rectangle
from settings import config


class TestDrawingSurface(unittest.TestCase):
    def test_translate_to_player(self):
        """
        Moves given location to the correct player corner
        """
        config.tabletop_size = Vector(1000, 500)
        config.player_area_size = Vector(200, 200)

        for player, l in [
            (0, (10, 10)),      # Top left hand corner
            (1, (810, 10)),     # Top right hand corner
            (2, (810, 310)),    # Bottom right hand corner
            (3, (10, 310))
        ]:
            self.assertEqual(translate_to_player(player, (10, 10)), l)

    def test_scale_vertices(self):
        """
        scales all values in a nested list
        """
        config.scaling_factor = 3
        self.assertEqual(
            scale_vertices([5, (10, 12, [3, 8], Vector(2, 3))]),
            [15, [30, 36, [9, 24], [6, 9]]]
        )

    def test_grow_rectangle(self):
        """
        Moves the rectangle and increases the size
        """
        self.assertEqual(
            grow_rectangle((50, 70, 30, 20), 4),
            (46, 66, 38, 28)
        )
