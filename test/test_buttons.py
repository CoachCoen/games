import unittest
from unittest.mock import MagicMock, patch

from buttons import ButtonCollection
from game_actions import AbstractAction
from game import game
from settings import config


class DummyAction(AbstractAction):
    pass


def dummy_function():
    pass


class TestButtonCollection(unittest.TestCase):
    def setUp(self):
        config.scaling_factor = 1

    @patch.object(game, 'refresh_display')
    def test_mouse_clicks(self, _):
        """
        A mouse click will trigger the button's activate() method,
        for any button at the mouse position
        """
        buttons = ButtonCollection()
        dummy_action = DummyAction()
        dummy_action.activate = MagicMock(return_value=dummy_function)
        buttons.add((0, 0, 10, 10), dummy_action)

        # Click outside the button, no call
        buttons.process_mouse_click((15, 15))
        self.assertEqual(dummy_action.activate.call_args_list, [])

        # Click the button, function called
        buttons.process_mouse_click((5, 5))
        dummy_action.activate.assert_any_call()

if __name__ == '__main__':
    unittest.main()
