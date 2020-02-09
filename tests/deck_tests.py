import unittest

from engine.card import Card
from engine.deck import Deck


class DeckTests(unittest.TestCase):
    def test_init_deck(self):
        deck = Deck()
        deck.initialize()
        deck_size = 56
        self.assertEqual(deck_size, len(deck.cards))
        self.assertTrue(isinstance(deck.cards, set))
        for card in deck.cards:
            self.assertTrue(isinstance(card, Card))
