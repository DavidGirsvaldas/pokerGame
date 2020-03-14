import unittest

from engine.game_settings import DefaultGameSettings


class DefaultGameSettingsTests(unittest.TestCase):


    def tests_get_default_setup(self):
        initial_stack = 5000
        game_settings = DefaultGameSettings()
        self.assertEqual(25, game_settings.small_blind_size)
        self.assertEqual(initial_stack, game_settings.initial_stack)
        self.assertEqual(5, len(game_settings.players))
        self.assertEqual("ConsolePlayer", game_settings.players[0].name)
        self.assertEqual("Player0", game_settings.players[1].name)
        self.assertEqual("Player1", game_settings.players[2].name)
        self.assertEqual("Player2", game_settings.players[3].name)
        self.assertEqual("Player3", game_settings.players[4].name)
        self.assertEqual(initial_stack, game_settings.players[0].stack)
        self.assertEqual(initial_stack, game_settings.players[1].stack)
        self.assertEqual(initial_stack, game_settings.players[2].stack)
        self.assertEqual(initial_stack, game_settings.players[3].stack)
        self.assertEqual(initial_stack, game_settings.players[4].stack)

