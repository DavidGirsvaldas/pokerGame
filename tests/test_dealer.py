import unittest

from engine.action import Action
from engine.deck import Deck
from engine.player import Player
from engine.dealer import Dealer
from engine.pot import Pot
from engine.seating import Seating
from tests.test_deck import DeckTests


class TestDealer(unittest.TestCase):

    def setup_new_player(self, initial_stack):
        player = Player()
        player.stack = initial_stack
        return player

    def action_check_call(self, required_total_player_contribution_to_pot):
        return Action.ACTION_CALL, required_total_player_contribution_to_pot

    def action_fold(self, _):
        return Action.ACTION_FOLD, 0

    def action_raise(self, new_required_total_player_contribution_to_pot):
        def player_action_raise(_):
            return Action.ACTION_RAISE, new_required_total_player_contribution_to_pot

        return player_action_raise

    def test_deal(self):
        player1 = Player()
        player2 = Player()
        seating = Seating([player1, player2])
        deck = Deck()
        deck.initialize()
        dealer = Dealer(deck, seating)
        dealer.deal()
        hand_size = 2
        cards_dealt = len(seating.players) * hand_size
        self.assertEqual(cards_dealt, len(set(player1.cards + player2.cards)))
        expected_remaining_card_count = DeckTests.deck_size - cards_dealt
        self.assertEqual(expected_remaining_card_count, len(deck.cards))

    def test_collect_blinds(self):
        initial_stack = 1000
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.pot = Pot()
        dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack, player1.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size, player3.stack)
        self.assertEqual(big_blind_size + small_blind_size, dealer.pot.size)
        dealer.move_button()
        dealer.pot = Pot()
        dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack - big_blind_size, player1.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size - small_blind_size, player3.stack)
        self.assertEqual(big_blind_size + small_blind_size, dealer.pot.size)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)

    def test_collect_blinds__when_player_dont_have_enough_chips(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        player1 = self.setup_new_player(100)
        player2 = self.setup_new_player(small_blind_size - 1)
        player3 = self.setup_new_player(big_blind_size - 1)
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.pot = Pot()
        dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack, player1.stack)
        self.assertEqual(0, player2.stack)
        self.assertEqual(0, player3.stack)
        self.assertEqual(13, dealer.pot.size)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)

    def test_move_button__when2players(self):
        player1 = Player()
        player2 = Player()
        seating = Seating([player1, player2])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.move_button()
        seating.button_pos = 0
        dealer.move_button()
        seating.button_pos = 1
        dealer.move_button()
        seating.button_pos = 0

    def test_move_button__when5players(self):
        player1 = Player()
        player2 = Player()
        player3 = Player()
        player4 = Player()
        player5 = Player()
        seating = Seating([player1, player2, player3, player4, player5])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.move_button()
        seating.button_pos = 0
        dealer.move_button()
        seating.button_pos = 1
        dealer.move_button()
        seating.button_pos = 2
        dealer.move_button()
        seating.button_pos = 3
        dealer.move_button()
        seating.button_pos = 4
        dealer.move_button()
        seating.button_pos = 5
        dealer.move_button()
        seating.button_pos = 0

    def test_setup_preflop(self):
        initial_stack = 100
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        pot = dealer.setup_preflop(small_blind_size)
        self.assertEqual(initial_stack, player1.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - small_blind_size * 2, player3.stack)
        self.assertEqual(small_blind_size * 3, dealer.pot.size)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)
        self.assertEqual(2, len(player1.cards))
        self.assertEqual(2, len(player2.cards))
        self.assertEqual(2, len(player3.cards))

    def test_preflop_round__when_all_fold(self):
        initial_stack = 100
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        player1.act = self.action_fold
        player2.act = self.action_fold
        player3.act = self.action_fold
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(player3, winner)
        self.assertEqual(105, player3.stack)

    def test_preflop_round__when_only_small_blind_plays(self):
        initial_stack = 100
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        player1.act = self.action_fold
        player2.act = self.action_check_call
        player3.act = self.action_fold
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(player2, winner)
        self.assertEqual(110, player2.stack)

    def test_preflop_round__when_only_utg_plays(self):
        initial_stack = 100
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        player1.act = self.action_check_call
        player2.act = self.action_fold
        player3.act = self.action_fold
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(player1, winner)
        self.assertEqual(115, player1.stack)

    def test_preflop_round__when_multiple_people_call(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        player1.act = self.action_check_call
        player2.act = self.action_fold
        player3.act = self.action_check_call
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(None, winner)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player2 not in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)
        self.assertEqual(initial_stack - big_blind_size, player1.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size, player3.stack)
        self.assertEqual(big_blind_size * 2 + small_blind_size, dealer.pot.size)
        self.assertEqual(3, len(dealer.community_cards))
        self.assertEqual(DeckTests.deck_size - len(seating.players) * 2 - 3, len(dealer.deck.cards))

    def test_preflop_round__when_player_bets__all_calls(self):
        initial_stack = 100
        bet_size = 50
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        player1.act = self.action_check_call
        player2.act = self.action_raise(bet_size)
        player3.act = self.action_check_call
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(None, winner)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size, player1.stack)
        self.assertEqual(initial_stack - bet_size, player2.stack)
        self.assertEqual(initial_stack - bet_size, player3.stack)
        self.assertEqual(bet_size * 3, dealer.pot.size)
        self.assertEqual(3, len(dealer.community_cards))
        self.assertEqual(DeckTests.deck_size - len(seating.players) * 2 - 3, len(dealer.deck.cards))

    def test_preflop_round__when_first_player_bets__all_calls(self):
        initial_stack = 100
        bet_size = 50
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        player1.act = self.action_raise(bet_size)
        player2.act = self.action_check_call
        player3.act = self.action_check_call
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(None, winner)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size, player1.stack)
        self.assertEqual(initial_stack - bet_size, player2.stack)
        self.assertEqual(initial_stack - bet_size, player3.stack)
        self.assertEqual(bet_size * 3, dealer.pot.size)
        self.assertEqual(3, len(dealer.community_cards))
        self.assertEqual(DeckTests.deck_size - len(seating.players) * 2 - 3, len(dealer.deck.cards))

    def test_preflop_round__when_player_raises__all_calls(self):
        initial_stack = 100
        bet_size = 50
        raise_size = bet_size + 10
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)

        def call_raise(amount):
            if amount == small_blind_size * 2:
                return Action.ACTION_CALL, amount
            return Action.ACTION_RAISE, raise_size

        player1.act = call_raise

        def raise_call(amount):
            if amount == small_blind_size * 2:
                return Action.ACTION_RAISE, bet_size
            return Action.ACTION_CALL, amount

        player2.act = raise_call
        player3.act = self.action_check_call
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(None, winner)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)
        self.assertEqual(initial_stack - raise_size, player1.stack)
        self.assertEqual(initial_stack - raise_size, player2.stack)
        self.assertEqual(initial_stack - raise_size, player3.stack)
        self.assertEqual(raise_size * 3, dealer.pot.size)
        self.assertEqual(3, len(dealer.community_cards))
        self.assertEqual(DeckTests.deck_size - len(seating.players) * 2 - 3, len(dealer.deck.cards))

    def test_playing_flop__when_all_fold__last_player_wins(self):
        initial_stack = 100
        small_blind_size = 5
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        players = [player1, player2, player3]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        player1.act = self.action_fold
        player2.act = self.action_fold
        player3.act = self.action_fold
        winner = dealer.play_flop()
        self.assertEqual(player1, winner)
        self.assertEqual(initial_stack + small_blind_size * 4, player1.stack)

    def test_playing_flop__when_all_checks(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind = small_blind_size * 2
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        players = [player1, player2, player3]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        winner = dealer.play_flop()
        self.assertEqual(None, winner)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)
        self.assertEqual(initial_stack - big_blind, player1.stack)
        self.assertEqual(initial_stack - big_blind, player2.stack)
        self.assertEqual(initial_stack - big_blind, player3.stack)
        self.assertEqual(big_blind * 3, dealer.pot.size)
        self.assertEqual(4, len(dealer.community_cards))
        self.assertEqual(DeckTests.deck_size - len(players) * 2 - 4, len(dealer.deck.cards))

    def test_playing_flop__when_player_bets__all_calls(self):
        initial_stack = 100
        bet_size = 40
        small_blind_size = 10
        big_blind_size = small_blind_size * 2
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        players = [player1, player2, player3]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        player1.act = self.action_check_call
        player2.act = self.action_raise(bet_size + big_blind_size)
        player3.act = self.action_check_call
        winner = dealer.play_flop()
        self.assertEqual(None, winner)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size, player1.stack)
        self.assertEqual(initial_stack - bet_size, player2.stack)
        self.assertEqual(initial_stack - bet_size, player3.stack)
        self.assertEqual(bet_size * 3, dealer.pot.size)
        self.assertEqual(4, len(dealer.community_cards))
        self.assertEqual(DeckTests.deck_size - len(players) * 2 - 4, len(dealer.deck.cards))

    def test_playing_flop__when_player_bets__one_folds_another_calls(self):
        initial_stack = 100
        small_blind_size = 10
        big_blind_size = small_blind_size * 2
        bet_size = 40
        player1 = self.setup_new_player(initial_stack)
        player2 = self.setup_new_player(initial_stack)
        player3 = self.setup_new_player(initial_stack)
        players = [player1, player2, player3]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)

        player1.act = self.action_check_call
        player2.act = self.action_raise(bet_size + big_blind_size)
        player3.act = self.action_fold
        winner = dealer.play_flop()
        self.assertEqual(None, winner)
        self.assertTrue(player1 in dealer.pot.players)
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 not in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size, player1.stack)
        self.assertEqual(initial_stack - bet_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size, player3.stack)
        self.assertEqual(bet_size * 2 + big_blind_size, dealer.pot.size)
        self.assertEqual(4, len(dealer.community_cards))
        self.assertEqual(DeckTests.deck_size - len(players) * 2 - 4, len(dealer.deck.cards))

    def setup_dealer_and_play_preflop_where_everybody_calls(self, players, small_blind_size):
        for player in players:
            player.act = self.action_check_call
        seating = Seating(players)
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.setup_preflop(small_blind_size)
        winner = dealer.preflop_round(small_blind_size)
        self.assertEqual(None, winner)
        return dealer
