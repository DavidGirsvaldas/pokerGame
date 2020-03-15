import unittest

from ..engine.combination import Combination
from ..engine.rank import Rank


class TestCombination(unittest.TestCase):

    def test_to_string_when_high_card(self):
        combination = Combination(1, [Rank.r7, Rank.r5, Rank.r4, Rank.r3, Rank.r2])
        result = str(combination)
        self.assertEqual("High card [7,5,4,3,2]", result)

    def test_to_string_when_pair(self):
        combination = Combination(2, [Rank.r2, Rank.r2, Rank.r5, Rank.r4, Rank.r3])
        result = str(combination)
        self.assertEqual("Pair [2,2,5,4,3]", result)

    def test_to_string_when_two_pairs(self):
        combination = Combination(3, [Rank.r3, Rank.r3, Rank.r2, Rank.r2, Rank.r4])
        result = str(combination)
        self.assertEqual("Two pairs [3,3,2,2,4]", result)

    def test_to_string_when_three_of_a_kind(self):
        combination = Combination(4, [Rank.r3, Rank.r3, Rank.r3, Rank.r4, Rank.r2])
        result = str(combination)
        self.assertEqual("Three of a kind [3,3,3,4,2]", result)

    def test_to_string_when_straight(self):
        combination = Combination(5, [Rank.r6, Rank.r5, Rank.r4, Rank.r3, Rank.r2])
        result = str(combination)
        self.assertEqual("Straight [6,5,4,3,2]", result)

    def test_to_string_when_flush(self):
        combination = Combination(6, [Rank.r7, Rank.r5, Rank.r4, Rank.r3, Rank.r2])
        result = str(combination)
        self.assertEqual("Flush [7,5,4,3,2]", result)
        
    def test_to_string_when_full_house(self):
        combination = Combination(7, [Rank.r3, Rank.r3, Rank.r3, Rank.r2, Rank.r2])
        result = str(combination)
        self.assertEqual("Full house [3,3,3,2,2]", result)

    def test_to_string_when_four_of_a_kind(self):
        combination = Combination(8, [Rank.r3, Rank.r3, Rank.r3, Rank.r3, Rank.r2])
        result = str(combination)
        self.assertEqual("Four of a kind [3,3,3,3,2]", result)

    def test_to_string_when_straight_flush(self):
        combination = Combination(9, [Rank.r6, Rank.r5, Rank.r4, Rank.r3, Rank.r2])
        result = str(combination)
        self.assertEqual("Straight flush [6,5,4,3,2]", result)

    def test_to_string_when_royal_flush(self):
        combination = Combination(10, [Rank.Ace, Rank.King, Rank.Queen, Rank.Jack, Rank.r10])
        result = str(combination)
        self.assertEqual("Royal flush [Ace,King,Queen,Jack,10]", result)