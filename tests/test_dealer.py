import unittest

from engine.action import Action
from engine.deck import Deck
from engine.player import Player
from engine.dealer import Dealer
from engine.seating import Seating
from tests.test_deck import DeckTests


class TestDealer(unittest.TestCase):

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
        player1 = Player()
        player1.stack = initial_stack
        player2 = Player()
        player2.stack = initial_stack
        player3 = Player()
        player3.stack = initial_stack
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        pot_size = dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack, player1.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size, player3.stack)
        self.assertEqual(big_blind_size + small_blind_size, pot_size.size)
        dealer.move_button()
        pot_size = dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack - big_blind_size, player1.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size - small_blind_size, player3.stack)
        self.assertEqual(big_blind_size + small_blind_size, pot_size.size)
        self.assertTrue(player1 in pot_size.players)
        self.assertTrue(player3 in pot_size.players)

    def test_collect_blinds__when_player_dont_have_enough_chips(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        player1 = Player()
        player1.stack = 100
        player2 = Player()
        player2.stack = small_blind_size - 1
        player3 = Player()
        player3.stack = big_blind_size - 1
        seating = Seating([player1, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        pot_size = dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack, player1.stack)
        self.assertEqual(0, player2.stack)
        self.assertEqual(0, player3.stack)
        self.assertEqual(13, pot_size.size)
        self.assertTrue(player2 in pot_size.players)
        self.assertTrue(player3 in pot_size.players)

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

    def test_preflop(self):
        initial_stack = 100
        small_blind_size = 5
        player1 = Player()
        player1.stack = initial_stack
        player2 = Player()
        player2.stack = initial_stack
        player3 = Player()
        player3.stack = initial_stack
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
        player1 = Player()
        player1.stack = initial_stack
        player1.act = lambda x: Action.ACTION_FOLD
        player2 = Player()
        player2.stack = initial_stack
        player2.act = lambda x: Action.ACTION_FOLD
        player3 = Player()
        player3.stack = initial_stack
        player3.act = lambda x: Action.ACTION_FOLD
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
        player1 = Player()
        player1.stack = initial_stack
        player1.act = lambda x: Action.ACTION_FOLD
        player2 = Player()
        player2.stack = initial_stack
        player2.act = lambda x: Action.ACTION_CALL
        player3 = Player()
        player3.stack = initial_stack
        player3.act = lambda x: Action.ACTION_FOLD
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
        player1 = Player()
        player1.stack = initial_stack
        player1.act = lambda x: Action.ACTION_CALL
        player2 = Player()
        player2.stack = initial_stack
        player2.act = lambda x: Action.ACTION_FOLD
        player3 = Player()
        player3.stack = initial_stack
        player3.act = lambda x: Action.ACTION_FOLD
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
        big_blind_size = small_blind_size *2
        player1 = Player()
        player1.stack = initial_stack
        player1.act = lambda x: Action.ACTION_CALL
        player2 = Player()
        player2.stack = initial_stack
        player2.act = lambda x: Action.ACTION_FOLD
        player3 = Player()
        player3.stack = initial_stack
        player3.act = lambda x: Action.ACTION_CHECK
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
