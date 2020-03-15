import unittest

from engine import combination_finder
from engine.card import Card
from engine.combination import Combination
from engine.rank import Rank
from engine.suit import Suit


class CombinationFinderTests(unittest.TestCase):
    def test_canFindHighCard(self):
        sc = Suit.clubs
        sd = Suit.diamonds
        ss = Suit.spades
        sh = Suit.hearths
        # 1
        test_input = [Card(Rank(2), sc), Card(Rank(10), sh), Card(Rank(13), ss), Card(Rank(4), sd), Card(Rank(3), sc),
                      Card(Rank(7), sc), Card(Rank(5), sc)]
        result = combination_finder.find(test_input)
        self.assertEqual(1, result.strength)
        self.assertEqual([Rank(13), Rank(10), Rank(7), Rank(5), Rank(4)], result.kickers)
        # 2
        test_input = [Card(Rank(13), sc), Card(Rank(10), sd), Card(Rank(3), sh), Card(Rank(2), sd), Card(Rank(7), sc),
                      Card(Rank(5), sc), Card(Rank(4), sc)]
        result = combination_finder.find(test_input)
        self.assertEqual(1, result.strength)
        self.assertEqual([Rank(13), Rank(10), Rank(7), Rank(5), Rank(4)], result.kickers)

    def test__find_four_of_a_kind(self):
        sc = Suit.clubs
        # when 4 of a kind found
        test_input = [Card(Rank(10), sc), Card(Rank(10), sc), Card(Rank(10), sc), Card(Rank(10), sc), Card(Rank(2), sc)]
        result = combination_finder.find(test_input)
        self.assertEqual(8, result.strength)
        self.assertEqual([Rank(10), Rank(10), Rank(10), Rank(10), Rank(2)], result.kickers)
        # when 4 of a kind found
        test_input = [Card(Rank(2), sc), Card(Rank(3), sc), Card(Rank(4), sc), Card(Rank(2), sc), Card(Rank(2), sc),
                      Card(Rank(2), sc), Card(Rank(4), sc)]
        result = combination_finder.find(test_input)
        self.assertEqual(8, result.strength)
        self.assertEqual([Rank(2), Rank(2), Rank(2), Rank(2), Rank(4)], result.kickers)

    def test__is_royal_flush(self):
        expected = Combination(10, [Rank.Ace, Rank.King, Rank.Queen, Rank.Jack, Rank.r10])
        sc = Suit.clubs
        sd = Suit.diamonds
        # when clubs
        test_input = [Card(Rank.Ace, sc), Card(Rank.r10, sc), Card(Rank.Queen, sc), Card(Rank.Jack, sc),
                      Card(Rank.King, sc)]
        result = combination_finder.find(test_input)
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)
        # when diamonds
        test_input = [Card(Rank.Ace, sd), Card(Rank.r10, sd), Card(Rank.King, sd), Card(Rank.Queen, sd),
                      Card(Rank.Jack, sd)]
        result = combination_finder.find(test_input)
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)

    def test__find_full_house(self):
        sc = Suit.clubs
        sd = Suit.diamonds
        ss = Suit.spades
        sh = Suit.hearths
        # when full house found then returns combo ordered by kickers
        test_input = [Card(Rank.Ace, sc), Card(Rank.Ace, sd), Card(Rank.Ace, ss), Card(Rank.King, sc),
                      Card(Rank.King, sh)]
        result = combination_finder.find(test_input)
        expected = Combination(7, [Rank.Ace, Rank.Ace, Rank.Ace, Rank.King, Rank.King])
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)

        # when full house found then returns combo ordered by kickers
        test_input = [Card(Rank.Jack, sc), Card(Rank.Jack, sd), Card(Rank.Jack, ss), Card(Rank.r10, sc),
                      Card(Rank.r10, sh)]
        result = combination_finder.find(test_input)
        expected = Combination(7, [Rank.Jack, Rank.Jack, Rank.Jack, Rank.r10, Rank.r10])
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)

        # when two full houses available then returns the higher
        test_input = [Card(Rank.r2, sh), Card(Rank.r3, sc), Card(Rank.r2, sc), Card(Rank.r3, sd), Card(Rank.r3, ss),
                      Card(Rank.r2, sd)]
        result = combination_finder.find(test_input)
        expected = Combination(7, [Rank.r3, Rank.r3, Rank.r3, Rank.r2, Rank.r2])
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)

    def test__find_flush(self):
        sh = Suit.hearths
        ss = Suit.spades
        # when 5 hearths flush then returns combo with kickers ordered by strength
        test_input = [Card(Rank.King, sh), Card(Rank.r2, sh), Card(Rank.r4, sh), Card(Rank.r5, sh), Card(Rank.r6, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(6, result.strength)
        self.assertEqual([Rank.King, Rank.r6, Rank.r5, Rank.r4, Rank.r2], result.kickers)

        # when 5 spades flush then returns combo with kickers ordered by strength
        test_input = [Card(Rank.r5, ss), Card(Rank.r10, ss), Card(Rank.Ace, ss), Card(Rank.r2, ss), Card(Rank.r6, ss)]
        result = combination_finder.find(test_input)
        self.assertEqual(6, result.strength)
        self.assertEqual([Rank.Ace, Rank.r10, Rank.r6, Rank.r5, Rank.r2], result.kickers)

        # when more than 5 cards in flush returns only strongest 5
        test_input = [Card(Rank.r5, sh), Card(Rank.r10, sh), Card(Rank.Ace, sh), Card(Rank.r2, sh), Card(Rank.r6, sh),
                      Card(Rank.Jack, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(6, result.strength)
        self.assertEqual([Rank.Ace, Rank.Jack, Rank.r10, Rank.r6, Rank.r5], result.kickers)

    def test_is_straight_flush(self):
        sh = Suit.hearths
        ss = Suit.spades
        # when 5 hearths straight flush then returns combo with kickers ordered by strength
        test_input = [Card(Rank.r6, sh), Card(Rank.Ace, ss), Card(Rank.r5, ss), Card(Rank.r5, sh), Card(Rank.r2, sh),
                      Card(Rank.r3, sh), Card(Rank.r4, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(9, result.strength)
        self.assertEqual([Rank.r6, Rank.r5, Rank.r4, Rank.r3, Rank.r2], result.kickers)
        # when 5 spade straight flush then returns combo with kickers ordered by strength
        test_input = [Card(Rank.King, ss), Card(Rank.r9, ss), Card(Rank.r10, ss), Card(Rank.Queen, ss),
                      Card(Rank.Jack, ss),
                      Card(Rank.r3, sh), Card(Rank.r4, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(9, result.strength)
        self.assertEqual([Rank.King, Rank.Queen, Rank.Jack, Rank.r10, Rank.r9], result.kickers)

    def test_is_straight(self):
        sh = Suit.hearths
        ss = Suit.spades
        # when straight then returns combo with kickers ordered by strength (1)
        test_input = [Card(Rank.r6, sh), Card(Rank.Queen, ss), Card(Rank.r5, ss), Card(Rank.r5, sh),
                      Card(Rank.r2, ss), Card(Rank.r3, sh), Card(Rank.r4, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(5, result.strength)
        self.assertEqual([Rank.r6, Rank.r5, Rank.r4, Rank.r3, Rank.r2], result.kickers)
        # when two straights available then returns with stronger kicker (2)
        test_input = [Card(Rank.King, sh), Card(Rank.r9, ss), Card(Rank.r10, ss), Card(Rank.Queen, ss),
                      Card(Rank.Jack, ss),
                      Card(Rank.r8, sh), Card(Rank.r7, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(5, result.strength)
        self.assertEqual([Rank.King, Rank.Queen, Rank.Jack, Rank.r10, Rank.r9], result.kickers)
        # when straight from Ace to 5
        test_input = [Card(Rank.r7, sh), Card(Rank.Ace, ss), Card(Rank.r5, ss), Card(Rank.r5, sh),
                      Card(Rank.r2, ss), Card(Rank.r3, sh), Card(Rank.r4, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(5, result.strength)
        self.assertEqual([Rank.r5, Rank.r4, Rank.r3, Rank.r2, Rank.Ace], result.kickers)

    def test_find_three_of_a_kind(self):
        sh = Suit.hearths
        ss = Suit.spades
        # when three of a kind found then returns combo with kickers ordered by strength (1)
        test_input = [Card(Rank.Jack, sh), Card(Rank.Ace, ss), Card(Rank.Jack, ss), Card(Rank.r5, sh),
                      Card(Rank.r2, ss), Card(Rank.Jack, sh), Card(Rank.r4, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(4, result.strength)
        self.assertEqual([Rank.Jack, Rank.Jack, Rank.Jack, Rank.Ace, Rank.r5], result.kickers)
        # when three of a kind found then returns combo with kickers ordered by strength (2)
        test_input = [Card(Rank.Ace, sh), Card(Rank.Ace, ss), Card(Rank.r3, ss), Card(Rank.r6, sh),
                      Card(Rank.r2, ss), Card(Rank.Ace, sh), Card(Rank.r4, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(4, result.strength)
        self.assertEqual([Rank.Ace, Rank.Ace, Rank.Ace, Rank.r6, Rank.r4], result.kickers)

    def test_find_two_pairs(self):
        sh = Suit.hearths
        ss = Suit.spades
        # when two pairs found then returns combo with highest kicker
        test_input = [Card(Rank.Queen, sh), Card(Rank.Ace, ss), Card(Rank.r2, ss), Card(Rank.r5, sh),
                      Card(Rank.r2, ss), Card(Rank.Queen, sh), Card(Rank.r4, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(3, result.strength)
        self.assertEqual([Rank.Queen, Rank.Queen, Rank.r2, Rank.r2, Rank.Ace], result.kickers)
        # when three pairs found then returns combo with highest pairs and highest kicker
        test_input = [Card(Rank.r10, sh), Card(Rank.r3, ss), Card(Rank.r2, ss), Card(Rank.r5, sh),
                      Card(Rank.r2, ss), Card(Rank.r4, sh), Card(Rank.r3, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(3, result.strength)
        self.assertEqual([Rank.r3, Rank.r3, Rank.r2, Rank.r2, Rank.r10], result.kickers)

    def test_find_pair(self):
        sh = Suit.hearths
        ss = Suit.spades
        # when pair found then returns combo with highest kickers (1)
        test_input = [Card(Rank.r9, sh), Card(Rank.Ace, ss), Card(Rank.King, ss), Card(Rank.r4, sh),
                      Card(Rank.r2, ss), Card(Rank.r9, sh), Card(Rank.r10, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(2, result.strength)
        self.assertEqual([Rank.r9, Rank.r9, Rank.Ace, Rank.King, Rank.r10], result.kickers)
        # when pair found then returns combo with highest kickers (2)
        test_input = [Card(Rank.Jack, sh), Card(Rank.Ace, ss), Card(Rank.King, ss), Card(Rank.r4, sh),
                      Card(Rank.r2, ss), Card(Rank.r10, sh), Card(Rank.Jack, sh)]
        result = combination_finder.find(test_input)
        self.assertEqual(2, result.strength)
        self.assertEqual([Rank.Jack, Rank.Jack, Rank.Ace, Rank.King, Rank.r10], result.kickers)


if __name__ == '__main__':
    unittest.main()
