import unittest

import combinations
from card import Card
from combination import Combination
from rank import Rank
from suit import Suit


class MyTestCase(unittest.TestCase):
    def test_canFindHighCard(self):
        test_input = [Rank(1), Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(7), Rank(8), Rank(9), Rank(10),
                      Rank(11),
                      Rank(12), Rank(13), Rank(14)]
        self.assertEqual(combinations.find_high_card(test_input), Rank.Ace)
        test_input = [Rank(1), Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(7), Rank(8), Rank(9), Rank(10),
                      Rank(11),
                      Rank(12), Rank(13)]
        self.assertEqual(combinations.find_high_card(test_input), Rank.King)
        test_input = [Rank(7), Rank(1), Rank(12), Rank(4), Rank(3), Rank(5), Rank(9), Rank(6), Rank(8)]
        self.assertEqual(combinations.find_high_card(test_input), Rank.Queen)

    def test__find_four_of_a_kind(self):
        test_input = [Rank(1), Rank(1), Rank(1), Rank(1)]
        self.assertEqual(combinations.find_four_of_a_kind(test_input), Rank(1))
        test_input = [Rank(1), Rank(1), Rank(1)]
        self.assertEqual(combinations.find_four_of_a_kind(test_input), None)
        test_input = [Rank(1), Rank(2), Rank(2), Rank(2), Rank(2)]
        self.assertEqual(combinations.find_four_of_a_kind(test_input), Rank(2))

    def test__is_royal_flush(self):
        sc = Suit.clubs
        sd = Suit.diamonds
        test_input = [Card(Rank.Ace, sc), Card(Rank.r10, sc), Card(Rank.Queen, sc), Card(Rank.Jack, sc),
                      Card(Rank.King, sc)]
        self.assertEqual(combinations.is_royal_flush(test_input), True)
        test_input = [Card(Rank.Ace, sd), Card(Rank.r10, sd), Card(Rank.King, sd), Card(Rank.Queen, sd),
                      Card(Rank.Jack, sd)]
        self.assertEqual(combinations.is_royal_flush(test_input), True)
        test_input = [Card(Rank.Ace, sc), Card(Rank.r10, sd), Card(Rank.Queen, sd), Card(Rank.Jack, sd),
                      Card(Rank.King, sd)]
        self.assertEqual(combinations.is_royal_flush(test_input), False)
        test_input = [Card(Rank.r10, sc), Card(Rank.r10, sc), Card(Rank.Queen, sc), Card(Rank.Jack, sc),
                      Card(Rank.King, sc)]
        self.assertEqual(combinations.is_royal_flush(test_input), False)
        test_input = [Card(Rank.Ace, sc), Card(Rank.r10, sc), Card(Rank.Queen, sc), Card(Rank.Jack, sc),
                      Card(Rank.r2, sc)]
        self.assertEqual(combinations.is_royal_flush(test_input), False)

    def test__return_full_house(self):
        sc = Suit.clubs
        sd = Suit.diamonds
        ss = Suit.spade
        sh = Suit.hearths
        test_input = [Card(Rank.Ace, sc), Card(Rank.Ace, sd), Card(Rank.Ace, ss), Card(Rank.King, sc),
                      Card(Rank.King, sh)]
        result = combinations.find_full_house(test_input)
        expected = Combination(7, [Rank.Ace, Rank.King])
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)

        test_input = [Card(Rank.Jack, sc), Card(Rank.Jack, sd), Card(Rank.Jack, ss), Card(Rank.r10, sc),
                      Card(Rank.r10, sh)]
        result = combinations.find_full_house(test_input)
        expected = Combination(7, [Rank.Jack, Rank.r10])
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)

        test_input = [Card(Rank.r2, sh), Card(Rank.r1, sc), Card(Rank.r2, sc), Card(Rank.r1, sd), Card(Rank.r1, ss)]
        result = combinations.find_full_house(test_input)
        expected = Combination(7, [Rank.r1, Rank.r2])
        self.assertEqual(expected.strength, result.strength)
        self.assertEqual(expected.kickers, result.kickers)

        test_input = [Card(Rank.r2, sh), Card(Rank.r1, sc), Card(Rank.r2, sc), Card(Rank.r1, sd), Card(Rank.r3, ss)]
        result = combinations.find_full_house(test_input)
        self.assertEqual(None, result)

    def test__find_flush(self):
        sh = Suit.hearths
        ss = Suit.spade
        # when 5 hearths flush then returns combo with kickers ordered by strength
        test_input = [Card(Rank.r1, sh), Card(Rank.r2, sh), Card(Rank.r4, sh), Card(Rank.r5, sh), Card(Rank.r6, sh)]
        result = combinations.find_flush(test_input)
        self.assertEqual(6, result.strength)
        self.assertEqual([Rank.r6, Rank.r5, Rank.r4, Rank.r2, Rank.r1], result.kickers)

        # when 5 spades flush then returns combo with kickers ordered by strength
        test_input = [Card(Rank.r5, ss), Card(Rank.r10, ss), Card(Rank.Ace, ss), Card(Rank.r1, ss), Card(Rank.r6, ss)]
        result = combinations.find_flush(test_input)
        self.assertEqual(6, result.strength)
        self.assertEqual([Rank.Ace, Rank.r10, Rank.r6, Rank.r5, Rank.r1], result.kickers)

        # when more than 5 cards in flush returns only strongest 5
        test_input = [Card(Rank.r5, sh), Card(Rank.r10, sh), Card(Rank.Ace, sh), Card(Rank.r1, sh), Card(Rank.r6, sh), Card(Rank.Jack, sh)]
        result = combinations.find_flush(test_input)
        self.assertEqual(6, result.strength)
        self.assertEqual([Rank.Ace, Rank.Jack, Rank.r10, Rank.r6, Rank.r5], result.kickers)

        # when only 4 cards in suit returns None
        test_input = [Card(Rank.r5, sh), Card(Rank.r10, sh), Card(Rank.Ace, sh), Card(Rank.r1, sh), Card(Rank.r6, ss)]
        result = combinations.find_flush(test_input)
        self.assertEqual(None, result)

if __name__ == '__main__':
    unittest.main()
