import unittest

from engine.game_settings import DefaultGameSettings


class DefaultGameSettingsTests(unittest.TestCase):


    def tests_get_default_setup(self):
        initial_stack = 800
        game_settings = DefaultGameSettings()
        self.assertEqual(25, game_settings.small_blind_size)
        self.assertEqual(initial_stack, game_settings.initial_stack)
        seating = game_settings.seating
        self.assertEqual(5, len(seating.players))
        self.assertEqual("Player0", seating.players[0].name)
        self.assertEqual("Player1", seating.players[1].name)
        self.assertEqual("Player2", seating.players[2].name)
        self.assertEqual("Player3", seating.players[3].name)
        self.assertEqual("ConsolePlayer", seating.players[4].name)
        self.assertEqual(initial_stack, seating.players[0].stack)
        self.assertEqual(initial_stack, seating.players[1].stack)
        self.assertEqual(initial_stack, seating.players[2].stack)
        self.assertEqual(initial_stack, seating.players[3].stack)
        self.assertEqual(initial_stack, seating.players[4].stack)

