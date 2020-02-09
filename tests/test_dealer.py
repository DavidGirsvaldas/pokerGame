import unittest

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
        self.assertEqual(cards_dealt, len(set(player1.hand + player2.hand)))
        expected_remaining_card_count = DeckTests.deck_size - cards_dealt
        self.assertEqual(expected_remaining_card_count, len(deck.cards))

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