import unittest
import combinations
from rank import Rank


class MyTestCase(unittest.TestCase):
    def test_canFindHighCard(self):
        test_input = [Rank(1), Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(7), Rank(8), Rank(9), Rank(10), Rank(11),
                 Rank(12), Rank(13), Rank(14)]
        self.assertEqual(combinations.find_high_card(test_input), Rank.Ace)
        test_input = [Rank(1), Rank(2), Rank(3), Rank(4), Rank(5), Rank(6), Rank(7), Rank(8), Rank(9), Rank(10), Rank(11),
                 Rank(12), Rank(13)]
        self.assertEqual(combinations.find_high_card(test_input), Rank.King)
        test_input = [Rank(7), Rank(1), Rank(12), Rank(4), Rank(3), Rank(5), Rank(9), Rank(6), Rank(8)]
        self.assertEqual(combinations.find_high_card(test_input), Rank.Queen)


if __name__ == '__main__':
    unittest.main()
