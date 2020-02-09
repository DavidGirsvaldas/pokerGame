import unittest

from engine.deck import Deck
from engine.player import Player
from engine.dealer import Dealer
from tests.test_deck import DeckTests


class TestDealer(unittest.TestCase):

    def test_start__players_receive_cards(self):
        player1 = Player()
        player2 = Player()
        players = [player1, player2]
        deck = Deck()
        deck.initialize()
        dealer = Dealer(deck, players)
        dealer.deal()
        hand_size = 2
        cards_dealt = len(players) * hand_size
        self.assertEqual(cards_dealt, len(set(player1.hand + player2.hand)))
        expected_remaining_card_count = DeckTests.deck_size - cards_dealt
        self.assertEqual(expected_remaining_card_count, len(deck.cards))
