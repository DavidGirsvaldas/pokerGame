import unittest

from engine.player import Player
from engine.seating import Seating


class TestSeating(unittest.TestCase):

    def test_big_blind_player__correctly_determines_big_blind_position(self):
        button_positions = [(0, "Player2"), (1, "Player3"), (2, "Player0"), (3, "Player1")]
        for button_position, big_blind_name in button_positions:
            with self.subTest():
                player0 = Player("Player0")
                player1 = Player("Player1")
                player2 = Player("Player2")
                player3 = Player("Player3")
                seating = Seating([player0, player1, player2, player3])
                seating.button_position = button_position
                result = seating.big_blind_player().name
                self.assertEqual(big_blind_name, result)
