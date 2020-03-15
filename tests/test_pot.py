import unittest

from engine.player import Player
from engine.pot import Pot


class TestPot(unittest.TestCase):

    def test_player_calls__when_player_allin_with_stack_that_is_too_small__side_pot_is_formed(self):
        player1 = Player("Player1", 1000)
        player2 = Player("Player2", 1000)
        player3 = Player("Player3", 80)
        pot = Pot()
        pot.player_calls(player1, 100)
        pot.player_calls(player2, 100)
        pot.player_calls(player3, 80)

        pots = pot.get_all_pots()
        self.assertEqual(2, len(pots))
        main_pot = pots[0]
        self.assertEqual(240, main_pot.pot_size())
        self.assertTrue(player1 in main_pot.players)
        self.assertTrue(player2 in main_pot.players)
        self.assertTrue(player3 in main_pot.players)

        side_pot = pots[1]
        self.assertEqual(40, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)

    def test_player_calls__when_players_allin_with_stack_that_is_too_small__side_pot_is_formed(self):
        player1 = Player("Player1", 1000)
        player2 = Player("Player2", 90)
        player3 = Player("Player3", 80)
        pot = Pot()
        pot.player_calls(player1, 100)
        pot.player_calls(player2, 90)
        pot.player_calls(player3, 70)

        pots = pot.get_all_pots()
        self.assertEqual(3, len(pots))
        main_pot = pots[0]
        self.assertEqual(210, main_pot.pot_size())
        self.assertTrue(player1 in main_pot.players)
        self.assertTrue(player2 in main_pot.players)
        self.assertTrue(player3 in main_pot.players)

        side_pot = pots[1]
        self.assertEqual(40, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)

        side_pot = pots[2]
        self.assertEqual(10, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 not in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)

    def test_player_calls__when_three_players_allin_with_stacks_that_are_too_small__three_side_pots_are_formed(self):
        player1 = Player("Player1", 1000)
        player2 = Player("Player2", 600)
        player3 = Player("Player3", 200)
        player4 = Player("Player4", 50)
        pot = Pot()
        pot.player_calls(player1, 999)
        pot.player_calls(player2, 600)
        pot.player_calls(player3, 200)
        pot.player_calls(player4, 50)

        pots = pot.get_all_pots()
        self.assertEqual(4, len(pots))
        main_pot = pots[0]
        self.assertEqual(200, main_pot.pot_size())
        self.assertTrue(player1 in main_pot.players)
        self.assertTrue(player2 in main_pot.players)
        self.assertTrue(player3 in main_pot.players)
        self.assertTrue(player4 in main_pot.players)

        side_pot = pots[1]
        self.assertEqual(450, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 in side_pot.players)
        self.assertTrue(player3 in side_pot.players)
        self.assertTrue(player4 not in side_pot.players)

        side_pot = pots[2]
        self.assertEqual(800, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)
        self.assertTrue(player4 not in side_pot.players)

        side_pot = pots[3]
        self.assertEqual(399, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 not in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)
        self.assertTrue(player4 not in side_pot.players)

    def test_player_calls__when_two_players_allin__two_side_pots_are_formed(self):
        player1 = Player("Player1", 1000)
        player2 = Player("Player2", 600)
        player3 = Player("Player3", 200)
        pot = Pot()
        pot.player_calls(player3, 200)
        pot.player_calls(player1, 999)
        pot.player_calls(player2, 600)

        pots = pot.get_all_pots()
        self.assertEqual(3, len(pots))
        main_pot = pots[0]
        self.assertEqual(600, main_pot.pot_size())
        self.assertTrue(player1 in main_pot.players)
        self.assertTrue(player2 in main_pot.players)
        self.assertTrue(player3 in main_pot.players)

        side_pot = pots[1]
        self.assertEqual(800, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)

        side_pot = pots[2]
        self.assertEqual(399, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 not in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)

    def test_player_calls__when_players_allin_after_placing_blinds(self):
        player1 = Player("Player1", 1000)
        player2 = Player("Player2", 600)
        player3 = Player("Player3", 200)
        pot = Pot()
        pot.player_calls(player2, 5)
        pot.player_calls(player3, 200)
        pot.player_calls(player1, 1000)
        pot.player_calls(player2, 600)

        pots = pot.get_all_pots()
        self.assertEqual(3, len(pots))
        main_pot = pots[0]
        self.assertEqual(600, main_pot.pot_size())
        self.assertTrue(player1 in main_pot.players)
        self.assertTrue(player2 in main_pot.players)
        self.assertTrue(player3 in main_pot.players)

        side_pot = pots[1]
        self.assertEqual(800, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)

        side_pot = pots[2]
        self.assertEqual(400, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 not in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)