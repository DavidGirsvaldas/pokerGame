import unittest

import card_showdown
from card import Card
from player import Player
from rank import Rank
from suit import Suit


class CardShowdownTests(unittest.TestCase):

    def test_find_winner__when2players__returns_winner(self):
        common_cards = [Card(Rank.r10, Suit.hearths), Card(Rank.Jack, Suit.diamonds), Card(Rank.Queen, Suit.diamonds),
                        Card(Rank.r2, Suit.spade), Card(Rank.r5, Suit.clubs)]
        player1 = Player([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.clubs)])  # has straight
        player2 = Player([Card(Rank.Jack, Suit.hearths), Card(Rank.Jack, Suit.clubs)])  # has three of a kind
        result = card_showdown.find_winner([player1, player2], common_cards)
        self.assertEqual(1, len(result))
        self.assertIn(player1, result)

    def test_find_winner__when3players__returns_winner(self):
        common_cards = [Card(Rank.r10, Suit.hearths), Card(Rank.Jack, Suit.diamonds), Card(Rank.Jack, Suit.diamonds),
                        Card(Rank.r2, Suit.spade), Card(Rank.r5, Suit.clubs)]
        player1 = Player([Card(Rank.r4, Suit.hearths), Card(Rank.r3, Suit.clubs)])  # has pair
        player2 = Player([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.spade)])  # has pair with highest kicker
        player3 = Player([Card(Rank.Ace, Suit.spade), Card(Rank.r1, Suit.clubs)])  # has pair
        result = card_showdown.find_winner([player1, player2, player3], common_cards)
        self.assertEqual(1, len(result))
        self.assertIn(player2, result)

    def test_find_winner__when2players_draw__returns_both_winners(self):
        common_cards = [Card(Rank.Jack, Suit.hearths), Card(Rank.Jack, Suit.diamonds),
                        Card(Rank.Jack, Suit.clubs),
                        Card(Rank.Ace, Suit.spade), Card(Rank.King, Suit.clubs)]
        player1 = Player([Card(Rank.r4, Suit.hearths), Card(Rank.r3, Suit.clubs)])  # hand doesnt play
        player2 = Player([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.spade)])  # has top full house
        player3 = Player([Card(Rank.Ace, Suit.diamonds), Card(Rank.r5, Suit.clubs)])  # has top full house
        result = card_showdown.find_winner([player1, player2, player3], common_cards)
        self.assertEqual(2, len(result))
        self.assertIn(player2, result)
        self.assertIn(player3, result)
