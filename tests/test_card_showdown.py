import unittest

from engine import card_showdown
from engine.card import Card
from engine.player import Player
from engine.rank import Rank
from engine.suit import Suit


class CardShowdownTests(unittest.TestCase):

    def test_find_winner__when_cards_missing__throws_exception(self):
        only_4_common_cards = [Card(Rank.r10, Suit.hearths), Card(Rank.Jack, Suit.diamonds),
                               Card(Rank.Queen, Suit.diamonds), Card(Rank.r2, Suit.spades)]
        player1 = self.init_test_player([Card(Rank.r2, Suit.hearths), Card(Rank.r3, Suit.clubs)])
        player2 = self.init_test_player([Card(Rank.r3, Suit.hearths), Card(Rank.r2, Suit.clubs)])
        self.assertRaises(ValueError, card_showdown.find_winners, [player1, player2], only_4_common_cards)

    def test_find_winner__when2players__returns_winner(self):
        common_cards = [Card(Rank.r10, Suit.hearths), Card(Rank.Jack, Suit.diamonds), Card(Rank.Queen, Suit.diamonds),
                        Card(Rank.r2, Suit.spades), Card(Rank.r5, Suit.clubs)]
        player1 = self.init_test_player([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.clubs)])  # has straight
        player2 = self.init_test_player([Card(Rank.Jack, Suit.hearths), Card(Rank.Jack, Suit.clubs)])  # has three of a kind
        result = card_showdown.find_winners([player1, player2], common_cards)
        self.assertEqual(1, len(result))
        self.assertIn(player1, result)

    def test_find_winner__when_player_has_higher_pair(self):
        common_cards = [Card(Rank.r3, Suit.spades), Card(Rank.King, Suit.clubs), Card(Rank.r10, Suit.diamonds),
                        Card(Rank.r5, Suit.spades), Card(Rank.r8, Suit.clubs)]
        player1 = self.init_test_player([Card(Rank.r6, Suit.diamonds), Card(Rank.r6, Suit.spades)])  # has pair of 6s
        player2 = self.init_test_player([Card(Rank.r3, Suit.hearths), Card(Rank.Jack, Suit.clubs)])  # has pair of 3s
        result = card_showdown.find_winners([player1, player2], common_cards)
        self.assertEqual(1, len(result))
        self.assertIn(player1, result)

    def test_find_winner__when3players__returns_winner(self):
        common_cards = [Card(Rank.r10, Suit.hearths), Card(Rank.Jack, Suit.diamonds), Card(Rank.Jack, Suit.diamonds),
                        Card(Rank.r2, Suit.spades), Card(Rank.r5, Suit.clubs)]
        player1 = self.init_test_player([Card(Rank.r4, Suit.hearths), Card(Rank.r3, Suit.clubs)])  # has pair of Jacks with kicker 10
        player2 = self.init_test_player([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.spades)])  # has pair of Jacks with kickers Ace, King
        player3 = self.init_test_player([Card(Rank.Ace, Suit.spades), Card(Rank.r3, Suit.clubs)])  # has pair of Jacks with kickers Ace, 10
        result = card_showdown.find_winners([player1, player2, player3], common_cards)
        self.assertEqual(1, len(result))
        self.assertIn(player2, result)

    def test_find_winner__when2players_draw__returns_both_winners(self):
        common_cards = [Card(Rank.Jack, Suit.hearths), Card(Rank.Jack, Suit.diamonds),
                        Card(Rank.Jack, Suit.clubs),
                        Card(Rank.Ace, Suit.spades), Card(Rank.King, Suit.clubs)]
        player1 = self.init_test_player([Card(Rank.r4, Suit.hearths), Card(Rank.r3, Suit.clubs)])  # hand doesnt play
        player2 = self.init_test_player([Card(Rank.Ace, Suit.hearths), Card(Rank.King, Suit.spades)])  # has top full house
        player3 = self.init_test_player([Card(Rank.Ace, Suit.diamonds), Card(Rank.r5, Suit.clubs)])  # has top full house
        result = card_showdown.find_winners([player1, player2, player3], common_cards)
        self.assertEqual(2, len(result))
        self.assertIn(player2, result)
        self.assertIn(player3, result)

    def init_test_player(self, cards):
        player = Player("Player")
        player.cards = cards
        return player
