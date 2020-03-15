import unittest

from engine.action import Action
from engine.dealer import Dealer
from engine.player import Player
from engine.round import Round
from engine.seating import Seating
from tests.test_dealer import TestDealer


class TestRound(unittest.TestCase):

    def setup_new_player(self, name, initial_stack):
        player = Player(name, initial_stack)
        return player

    def action_raise(self, raise_amount):
        def player_action_raise(amount):
            return Action.ACTION_RAISE, amount + raise_amount

        return player_action_raise

    def test_play_round__when_played_with_fixed_deck_and_player_keeps_raising__expected_player_wins(self):
        initial_stack = 1000
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        utg_player = self.setup_new_player("UTG", initial_stack)
        button_player.act = TestDealer.action_check_call()
        sb_player.act = TestDealer.action_check_call()
        bb_player.act = self.action_raise(10)
        utg_player.act = TestDealer.action_check_call()
        seating = Seating([button_player, sb_player, bb_player, utg_player])
        # seed value 2 results in shuffling where SmallBlind has best hand (Pair)
        seed = 2
        dealer = Dealer(None, seating, seed)
        round = Round(dealer)
        round.play_round(5)
        self.assertEqual(1150, sb_player.stack)

    def test_play_round__when_player_wins_in_preflop__round_concludes(self):
        initial_stack = 1000
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        utg_player = self.setup_new_player("UTG", initial_stack)
        button_player.act = TestDealer.action_fold()
        sb_player.act = TestDealer.action_fold()
        bb_player.act = TestDealer.action_fold()
        utg_player.act = TestDealer.action_fold()
        seating = Seating([button_player, sb_player, bb_player, utg_player])
        dealer = Dealer(None, seating)
        round = Round(dealer)
        round.play_round(5)
        self.assertEqual(0, len(dealer.community_cards))

    def test_play_round__when_player_wins_in_flop__round_concludes(self):
        initial_stack = 1000
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        utg_player = self.setup_new_player("UTG", initial_stack)
        button_player.act = TestDealer.action_call_fold(1)
        sb_player.act = TestDealer.action_call_fold(1)
        bb_player.act = TestDealer.action_call_fold(1)
        utg_player.act = TestDealer.action_call_fold(1)
        seating = Seating([button_player, sb_player, bb_player, utg_player])
        dealer = Dealer(None, seating)
        round = Round(dealer)
        winner = round.play_round(5)
        self.assertEqual(3, len(dealer.community_cards))

    def test_play_round__when_player_wins_in_turn__round_concludes(self):
        initial_stack = 1000
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        utg_player = self.setup_new_player("UTG", initial_stack)
        button_player.act = TestDealer.action_call_fold(2)
        sb_player.act = TestDealer.action_call_fold(2)
        bb_player.act = TestDealer.action_call_fold(2)
        utg_player.act = TestDealer.action_call_fold(2)
        seating = Seating([button_player, sb_player, bb_player, utg_player])
        dealer = Dealer(None, seating)
        round = Round(dealer)
        round.play_round(5)
        self.assertEqual(4, len(dealer.community_cards))

    def test_play_round__when_players_allin_with_unequal_stacks___side_pots_are_formed(self):
        stack_player1 = 1000
        stack_player2 = 3300
        stack_player3 = 7500
        stack_player4 = 30000
        player1 = self.setup_new_player("Button", stack_player1)
        player2 = self.setup_new_player("SmallBlind", stack_player2)
        player3 = self.setup_new_player("BigBlind", stack_player3)
        player4 = self.setup_new_player("UTG", stack_player4)
        player1.act = TestDealer.action_raise(stack_player1)
        player2.act = TestDealer.action_raise(stack_player2)
        player3.act = TestDealer.action_raise(stack_player3)
        player4.act = TestDealer.action_raise(stack_player4)
        seating = Seating([player1, player2, player3, player4])
        dealer = Dealer(None, seating, 1)
        # with seed 1 SmallBlind wins with pair of 6s
        # side pot goes to UTG with pair of 4s
        round = Round(dealer)
        round.play_round(5)
        self.assertEqual(0, player1.stack)
        self.assertEqual(stack_player2 * 3 + stack_player1, player2.stack)
        self.assertEqual(0, player3.stack)
        self.assertEqual(stack_player4 - stack_player2 * 2 + stack_player3, player4.stack)

    def test_play_round__when_draw___pot_is_shared(self):
        stack_player1 = 10000
        stack_player2 = 3000
        stack_player3 = 1001 # 1 chip will be dropped when splitting pot
        player1 = self.setup_new_player("Button", stack_player1)
        player2 = self.setup_new_player("SmallBlind", stack_player2)
        player3 = self.setup_new_player("BigBlind", stack_player3)
        player1.act = TestDealer.action_raise(stack_player3)
        player2.act = TestDealer.action_raise(stack_player2)
        player3.act = TestDealer.action_raise(stack_player3)
        seating = Seating([player1, player2, player3])
        dealer = Dealer(None, seating, 27)
        # draw for Button and SmallBlind, both have 2 pairs with same kicker
        round = Round(dealer)
        round.play_round(5)
        self.assertEqual(stack_player1 + 500, player1.stack)
        self.assertEqual(stack_player2 + 500, player2.stack)
        self.assertEqual(0, player3.stack)