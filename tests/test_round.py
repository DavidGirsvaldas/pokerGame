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
        winner = round.play_round()
        self.assertEqual("SmallBlind", winner.name)
        self.assertEqual(1150, winner.stack)

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
        winner = round.play_round()
        self.assertEqual("BigBlind", winner.name)

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
        winner = round.play_round()
        self.assertEqual("Button", winner.name)

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
        winner = round.play_round()
        self.assertEqual("Button", winner.name)