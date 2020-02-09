import unittest

from engine import card_showdown
from engine.card import Card
from engine.player import Player
from engine.rank import Rank
from engine.suit import Suit


class CardShowdownTests(unittest.TestCase):

    def test_find_winner__when2players__returns_winner(self):
        common_cards = [Card(Rank.r10, Suit.hearths), Card(Rank.Jack, Suit.diamonds), Card(Rank.Queen, Suit.diamonds),
                        Card(Rank.r2, Suit.spade), Card(Rank.r5, Suit.clubs)]
        player1 = Player()  # has straight
        player1.receive_cards([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.clubs)])
        player2 = Player()  # has three of a kind
        player2.receive_cards([Card(Rank.Jack, Suit.hearths), Card(Rank.Jack, Suit.clubs)])
        result = card_showdown.find_winner([player1, player2], common_cards)
        self.assertEqual(1, len(result))
        self.assertIn(player1, result)

    def test_find_winner__when3players__returns_winner(self):
        common_cards = [Card(Rank.r10, Suit.hearths), Card(Rank.Jack, Suit.diamonds), Card(Rank.Jack, Suit.diamonds),
                        Card(Rank.r2, Suit.spade), Card(Rank.r5, Suit.clubs)]
        player1 = Player()  # has pair
        player1.receive_cards([Card(Rank.r4, Suit.hearths), Card(Rank.r3, Suit.clubs)])
        player2 = Player()  # has pair with highest kicker
        player2.receive_cards([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.spade)])
        player3 = Player()  # has pair
        player3.receive_cards([Card(Rank.Ace, Suit.spade), Card(Rank.r1, Suit.clubs)])
        result = card_showdown.find_winner([player1, player2, player3], common_cards)
        self.assertEqual(1, len(result))
        self.assertIn(player2, result)

    def test_find_winner__when2players_draw__returns_both_winners(self):
        common_cards = [Card(Rank.Jack, Suit.hearths), Card(Rank.Jack, Suit.diamonds),
                        Card(Rank.Jack, Suit.clubs),
                        Card(Rank.Ace, Suit.spade), Card(Rank.King, Suit.clubs)]
        player1 = Player()  # hand doesnt play
        player1.receive_cards([Card(Rank.r4, Suit.hearths), Card(Rank.r3, Suit.clubs)])
        player2 = Player()  # has top full house
        player2.receive_cards([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.spade)])
        player3 = Player()  # has top full house
        player3.receive_cards([Card(Rank.Ace, Suit.diamonds), Card(Rank.r5, Suit.clubs)])
        result = card_showdown.find_winner([player1, player2, player3], common_cards)
        self.assertEqual(2, len(result))
        self.assertIn(player2, result)
        self.assertIn(player3, result)
