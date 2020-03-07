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

        self.assertEqual(2, len(pot.pots))
        main_pot = pot.pots[0]
        self.assertEqual(240, main_pot.pot_size())
        self.assertTrue(player1 in main_pot.players)
        self.assertTrue(player2 in main_pot.players)
        self.assertTrue(player3 in main_pot.players)

        side_pot = pot.pots[1]
        self.assertEqual(40, side_pot.pot_size())
        self.assertTrue(player1 in side_pot.players)
        self.assertTrue(player2 in side_pot.players)
        self.assertTrue(player3 not in side_pot.players)

    # def test_player_calls__when_two_players_allin_with_stacks_that_are_too_small__two_side_pots_is_formed(self):
    #     player1 = Player("Player1", 1000)
    #     player2 = Player("Player2", 90)
    #     player3 = Player("Player3", 80)
    #     pot = Pot()
    #     pot.player_calls(player1, 100)
    #     pot.player_calls(player2, 100)
    #     pot.player_calls(player3, 80)
    #
    #     self.assertEqual(2, len(pot.pots))
    #     main_pot = pot.pots[0]
    #     self.assertEqual(240, main_pot.pot_size())
    #     self.assertTrue(player1 in main_pot.players)
    #     self.assertTrue(player2 in main_pot.players)
    #     self.assertTrue(player3 in main_pot.players)
    #
    #     side_pot = pot.pots[1]
    #     self.assertEqual(40, side_pot.pot_size())
    #     self.assertTrue(player1 in side_pot.players)
    #     self.assertTrue(player2 in side_pot.players)
    #     self.assertTrue(player3 not in side_pot.players)