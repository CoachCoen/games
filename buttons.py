from graphics import scale_vertices, draw_rectangle, draw_text, \
    grow_rectangle, translate_to_player
from graphics import ColourPalette
from settings import Vector, config
from game import game


class ButtonCollection:
    """
    A list of buttons - which can respond to a mouse click by
    executing the action which corresponds with the mouse's location
    """

    def __init__(self):
        """
        Start with an empty list
        """
        self.buttons = []

    def add(self, rectangle, action, text=None, player_order=None):
        """
        :param rectangle: The area which will respond to a mouse click
        :param action: (subclass of AbstractAction) action to take
            when mouse is clicked
        :param text: If specified, show this as an actual button,
            including the text
        :param player_order: If specified, show in the specified
            player corner
        :return: the button (class Button) that this created
        """
        button = VisibleButton(rectangle, action, text, player_order) if text \
            else Button(rectangle, action, player_order)
        self.buttons.append(button)
        return button

    def process_mouse_click(self, mouse_position):
        """
        Process the action for any button in self.buttons with the mouse click
            position inside the button's rectangle
        :param mouse_position: The (x, y) coordinates of the mouse
        """

        # If the game state changed, refresh the screen
        if any(
                button.action.activate()
                for button in self.buttons
                if button.clicked(mouse_position)
        ):
            game.embody()

    def reset(self):
        self.__init__()


class Button:
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

    # TODO: Ideally this should be in embody.py, but this creates a circular reference
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

