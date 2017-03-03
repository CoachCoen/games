from game_state import game


class AbstractAction(object):
    pass


class MoveComponentToHoldingArea(AbstractAction):
    def __init__(self, component):
        self.component = component

    def activate(self):
        self.component.move_to_holding_area()
        game.current_player.take_component()
        return True


class ReturnComponent(AbstractAction):
    def __init__(self, component):
        self.component = component

    def activate(self):
        self.component.return_to_previous_position()
        game.current_player.return_component()
        return True


class Confirm(AbstractAction):
    @staticmethod
    def activate():
        game.current_player.confirm()
        return True


class Cancel(AbstractAction):
    @staticmethod
    def activate():
        game.current_player.cancel()
        return True
