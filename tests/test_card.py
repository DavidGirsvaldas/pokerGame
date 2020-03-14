import unittest

from engine.card import Card
from engine.rank import Rank
from engine.suit import Suit


class TestCard(unittest.TestCase):

    def test_to_string__correct_suite_name(self):
        card = Card(Rank.Ace, Suit.diamonds)
        self.assertEqual("Ace of diamonds", str(card))
        card = Card(Rank.Ace, Suit.hearths)
        self.assertEqual("Ace of hearts", str(card))
        card = Card(Rank.Ace, Suit.clubs)
        self.assertEqual("Ace of clubs", str(card))
        card = Card(Rank.Ace, Suit.spades)
        self.assertEqual("Ace of spades", str(card))

    def test_to_string__correct_rank_name(self):
        card = Card(Rank.Ace, Suit.diamonds)
        self.assertEqual("Ace of diamonds", str(card))
        card = Card(Rank.King, Suit.diamonds)
        self.assertEqual("King of diamonds", str(card))
        card = Card(Rank.Queen, Suit.diamonds)
        self.assertEqual("Queen of diamonds", str(card))
        card = Card(Rank.Jack, Suit.diamonds)
        self.assertEqual("Jack of diamonds", str(card))
        card = Card(Rank.r10, Suit.diamonds)
        self.assertEqual("10 of diamonds", str(card))
        card = Card(Rank.r2, Suit.diamonds)
        self.assertEqual("2 of diamonds", str(card))
