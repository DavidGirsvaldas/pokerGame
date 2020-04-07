import unittest

from pypokerengine.engine.card import Card

from engine.action import Action
from engine.computer_player import ComputerPlayer
from engine.rank import Rank
from engine.suit import Suit


class TestComputerPlayer(unittest.TestCase):

    def test_act__when_chances_to_win_small_and_call_is_required__fold(self):
        cards = [Card(Suit.diamonds, Rank.r2), Card(Suit.diamonds, Rank.r10), ]
        community_cards = []

        def mock_estimation(cards1, community_cards1):
            if cards1 == [Card.from_str("D2"), Card.from_str("DT")] and community_cards1 == []:
                return 0.1
            raise Exception("Bad arguments passed in test")

        player = ComputerPlayer("myComputer", 100)
        player.estimate_winrate = mock_estimation
        player.money_in_pot = 0
        player.receive_cards(cards)
        player.see_community_cards(community_cards)
        decision, amount = player.act(10)
        self.assertEqual(Action.ACTION_FOLD, decision)
        self.assertEqual(0, amount)

    def test_act__when_chances_to_win_small_and_check_is_available__check(self):
        cards = [Card(Suit.diamonds, Rank.r3), Card(Suit.diamonds, Rank.r9), ]
        community_cards = [Card(Suit.hearts, Rank.r6), Card(Suit.hearts, Rank.r7), Card(Suit.hearts, Rank.r8)]

        def mock_estimation(cards1, community_cards1):
            if cards1 == [Card.from_str("D3"), Card.from_str("D9")] and community_cards1 == [Card.from_str("H6"), Card.from_str("H7"), Card.from_str("H8")]:
                return 0.1
            raise Exception("Bad arguments passed in test")

        player = ComputerPlayer("myComputer", 100)
        player.estimate_winrate = mock_estimation
        player.money_in_pot = 10
        player.receive_cards(cards)
        player.see_community_cards(community_cards)
        decision, amount = player.act(10)
        self.assertEqual(Action.ACTION_CALL, decision)
        self.assertEqual(10, amount)

    def test_act__when_chances_to_win_high__raise(self):
        cards = [Card(Suit.diamonds, Rank.Ace), Card(Suit.diamonds, Rank.King), ]
        community_cards = []

        def mock_estimation(cards1, community_cards1):
            if cards1 == [Card.from_str("DA"), Card.from_str("DK")] and community_cards1 == []:
                return 0.31
            raise Exception("Bad arguments passed in test")

        player = ComputerPlayer("myComputer", 200)
        player.estimate_winrate = mock_estimation
        player.money_in_pot = 10
        player.receive_cards(cards)
        player.see_community_cards(community_cards)
        decision, amount = player.act(10)
        self.assertEqual(Action.ACTION_RAISE, decision)
        self.assertEqual(110, amount)

    def test_act__when_chances_to_win_high_but_funds_low__all_in(self):
        cards = [Card(Suit.diamonds, Rank.Ace), Card(Suit.diamonds, Rank.King), ]
        community_cards = []

        def mock_estimation(cards1, community_cards1):
            if cards1 == [Card.from_str("DA"), Card.from_str("DK")] and community_cards1 == []:
                return 0.31
            raise Exception("Bad arguments passed in test")

        player = ComputerPlayer("myComputer", 50)
        player.estimate_winrate = mock_estimation
        player.money_in_pot = 10
        player.receive_cards(cards)
        player.see_community_cards(community_cards)
        decision, amount = player.act(100)
        self.assertEqual(Action.ACTION_CALL, decision)
        self.assertEqual(60, amount)

    def test_act__when_odds_average__call(self):
        cards = [Card(Suit.diamonds, Rank.Ace), Card(Suit.diamonds, Rank.King), ]
        community_cards = []

        def mock_estimation(cards1, community_cards1):
            if cards1 == [Card.from_str("DA"), Card.from_str("DK")] and community_cards1 == []:
                return 0.2
            raise Exception("Bad arguments passed in test")

        player = ComputerPlayer("myComputer", 100)
        player.estimate_winrate = mock_estimation
        player.money_in_pot = 0
        player.receive_cards(cards)
        player.see_community_cards(community_cards)
        decision, amount = player.act(10)
        self.assertEqual(Action.ACTION_CALL, decision)
        self.assertEqual(10, amount)
