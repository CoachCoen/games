from game import game
from util_classes import PlayerStates


class AbstractAction:
    pass


class ToDo(AbstractAction):
    """
    A list of things to do when a button gets pressed
    """

    def __init__(self, actions):
        """
        Store the actions to execute later

        :param actions: The actions
        :type actions: list(callables)
        """
        self.actions = actions

    def activate(self):
        """
        Execute all the callables

        :return: True, to trigger a screen redraw
        """
        for action in self.actions:
            action()
        return True


class Confirm(AbstractAction):
    """
    Confirm the user's action
    """

    @staticmethod
    def activate():
        """
        Confirm the user's action (selected pieces)

        :return: True, to trigger a screen redraw
        """
        game.current_player.confirm()

        # TODO: All AbstractActions return True. Remove this if possible
        return True


class Cancel(AbstractAction):
    """
    Cancel the user's action - return the pieces to their original location
    """
    @staticmethod
    def activate():
        """
        Return the pieces to where they came from

        :return: True, to trigger a screen redraw
        """
        for component in game.components.holding_area_components:
            if game.current_player.state == PlayerStates.too_many_chips:
                component.to_player_area()
            else:
                component.move_back()
        return True
