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
        Add a button, as specified, to this collection

        :param rectangle: The area which will respond to a mouse click
        :param action: (subclass of AbstractAction) action to take
            when mouse is clicked
        :param text: If specified, show this as an actual button,
            including the text
        :param int player_order: If specified, show in the specified
            player corner
        :return: the button (class Button) that this created
        :rtype: Button/VisibleButton
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
    """
    Defines an action to be executed when a mouse click
    happens inside a specific rectangle (relative to a player's
    area, if specified)
    """
    def __init__(self, rectangle, action, player_order=None):
        """
        Initialise the instance

        :param Vector rectangle: The rectangle to click in
        :param game_actions.AbstractAction action: The Action
        :param int/None player_order: which player area to use, if any
        """
        if player_order is not None:
            rectangle = translate_to_player(player_order, rectangle)

        self.rectangle = rectangle
        self.action = action

    @property
    def scaled_rectangle(self):
        """
        Slightly larger version of the button area.
        Used to draw a line around the game piece, to show it is a button

        :return: slightly larger version of self.rectangle
        :rtype: vector.Vector
        """
        return scale_vertices(self.rectangle)

    def clicked(self, mouse_position):
        """
        Was the mouse clicked within this button's rectangle

        :param mouse_position: The position of the mouse click
        :type mouse_position: `int x, int y`
        :return: True if this button was clicked on
        :rtype: bool
        """

        return self.scaled_rectangle[0] <= mouse_position[0] <= \
            self.scaled_rectangle[0] + self.scaled_rectangle[2] and \
            self.scaled_rectangle[1] <= mouse_position[1] <= \
            self.scaled_rectangle[1] + self.scaled_rectangle[3]

    # Putting this in embody.py creates a circular reference
    def embody(self):
        """
        Embody (draw) the button
        """
        self._draw()

    def _draw(self):
        draw_rectangle(
            grow_rectangle(self.rectangle, 2),
            ColourPalette.button,
        )


class VisibleButton(Button):
    """
    A conventional button: rectangle with text
    """

    def __init__(self, rectangle, action, text, player_order):
        """

        :param rectangle: The area to draw and respond to
        :type rectangle: vector.Vector(left, top, right, bottom)
        :param action: Action to take when the button is clicked
        :type action: subclasses of game_actions.AbstractAction
        :param str text: Text to show on the button
        :param int player_order: If specified, show in the specified
            player corner
        """
        super().__init__(rectangle, action)
        self.text = text
        self.player_order = player_order

    def _draw(self):
        """
        Draw the button rectangle and text
        """
        draw_rectangle(self.rectangle, ColourPalette.button)
        draw_text(Vector(self.rectangle[0], self.rectangle[1]) +
                  config.button_text_location,
                  self.text)
