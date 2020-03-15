import unittest

from ..engine.card import Card
from ..engine.deck import Deck


class TestDeck(unittest.TestCase):
    deck_size = 52

    def test_init_deck(self):
        deck = Deck()
        deck.initialize()
        unique_cards = set(deck.cards)
        self.assertEqual(self.deck_size, len(unique_cards))
        for card in unique_cards:
            self.assertTrue(isinstance(card, Card))

    def test_shuffle(self):
        def is_deck_shuffled(list1, list2):
            is_different = False
            for i in range(len(list1)):
                if list1[i] != list2[i]:
                    is_different = True
            return is_different

        deck = Deck()
        deck.initialize()
        list_of_cards1 = list(deck.cards)
        deck.shuffle()
        list_of_cards2 = list(deck.cards)
        self.assertTrue(is_deck_shuffled(list_of_cards1, list_of_cards2))
        deck.shuffle()
        list_of_cards3 = list(deck.cards)
        self.assertTrue(is_deck_shuffled(list_of_cards3, list_of_cards2))
