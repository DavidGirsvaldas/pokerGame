import unittest

from engine.player import Player


class TestPlayer(unittest.TestCase):

    def test_str__prints_players_name_and_chip_count__1(self):
        player = Player("testName", 1000)
        result = str(player)
        self.assertEqual("testName (1000)", result)

    def test_str__prints_players_name_and_chip_count__2(self):
        player = Player("player1", 100)
        result = str(player)
        self.assertEqual("player1 (100)", result)
