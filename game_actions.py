from game import game


class AbstractAction:
    pass


class ToDo(AbstractAction):
    """
    A list of things to do (when a button gets pressed)
    """
    def __init__(self, actions):
        self.actions = actions

    def activate(self):
        for action in self.actions:
            action()
        return True


# class ConfirmTile(AbstractAction):
#     @staticmethod
#     def activate():
#         game.current_player.take_tile()
#

class Confirm(AbstractAction):
    """
    Confirm the user's action
    """
    # TODO: Move this into the ToDo class?
    @staticmethod
    def activate():
        game.current_player.confirm()
        return True


# class CancelTile(AbstractAction):
#     @staticmethod
#     def activate():
#         game.current_player.cancel_tile()
#

class Cancel(AbstractAction):
    """
    Cancel the user's action - return the pieces to their original location
    """
    # TODO: Move this into the ToDo class?
    @staticmethod
    def activate():
        game.current_player.cancel()
        return True
