import pygame

from drawing_surface import scale_vertices, draw_rectangle, draw_text, \
    grow_rectangle, translate_to_player
from drawing_surface import ColourPalette
from settings import Vector, config
from game_state import game


class ButtonCollection(object):
    def __init__(self):
        self.buttons = []

    def add(self, rectangle, action, text=None, player_order=None):
        button = VisibleButton(rectangle, action, text, player_order) if text \
            else Button(rectangle, action, player_order)
        self.buttons.append(button)
        return button

    def process_mouse_click(self, mouse_position):

        if any(
                button.action.activate()
                for button in self.buttons
                if button.clicked(mouse_position)
        ):
            # game.refresh_state()
            game.refresh_display()

    def reset(self):
        self.__init__()


class Button(object):
    def __init__(self, rectangle, action, player_order=None):
        # TODO: ?? Move player_order further down - make consistent
        if player_order is not None:
            rectangle = translate_to_player(player_order, rectangle)

        self.rectangle = rectangle
        self.action = action

    @property
    def scaled_rectangle(self):
        return scale_vertices(self.rectangle)

    def clicked(self, mouse_position):
        return self.scaled_rectangle[0] <= \
               mouse_position[0] <= \
               self.scaled_rectangle[0] + self.scaled_rectangle[2] and \
               self.scaled_rectangle[1] <= \
               mouse_position[1] <= \
               self.scaled_rectangle[1] + self.scaled_rectangle[3]

    def embody(self):
        self._draw()

    def _draw(self):
        draw_rectangle(
            grow_rectangle(self.rectangle, 2),
            ColourPalette.button,
        )


class VisibleButton(Button):
    def __init__(self, rectangle, action, text, player_order):

        super().__init__(rectangle, action)
        self.text = text
        self.player_order = player_order

    def _draw(self):
        draw_rectangle(self.rectangle, ColourPalette.button)
        draw_text(Vector(self.rectangle[0], self.rectangle[1]) +
                  config.button_text_location,
                  self.text)

buttons = ButtonCollection()
