import unittest
from unittest.mock import patch

from ..engine.console_player import ConsolePlayer
from ..engine.action import Action


class TestConsolePlayer(unittest.TestCase):

    @patch('builtins.input', lambda *args: '0')
    def test_act__when_user_folds(self):
        required_to_call = 10
        player = ConsolePlayer("ConsolePlayer")
        action, amount = player.act(required_to_call)
        self.assertEqual(Action.ACTION_FOLD, action)
        self.assertEqual(0, amount)

    @patch('builtins.input', lambda *args: '10')
    def test_act__when_user_calls(self):
        required_to_call = 10
        player = ConsolePlayer("ConsolePlayer")
        action, amount = player.act(required_to_call)
        self.assertEqual(Action.ACTION_CALL, action)
        self.assertEqual(10, amount)

    @patch('builtins.input', lambda *args: '20')
    def test_act__when_user_raises(self):
        required_to_call = 10
        player = ConsolePlayer("ConsolePlayer")
        action, amount = player.act(required_to_call)
        self.assertEqual(Action.ACTION_RAISE, action)
        self.assertEqual(20, amount)
