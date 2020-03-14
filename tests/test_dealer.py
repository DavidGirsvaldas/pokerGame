import unittest

from engine.action import Action
from engine.dealer import Dealer
from engine.deck import Deck
from engine.player import Player
from engine.pot import Pot
from engine.seating import Seating
from tests.test_deck import TestDeck


class TestDealer(unittest.TestCase):

    def setup_new_player(self, name, initial_stack):
        player = Player(name, initial_stack)
        return player

    @staticmethod
    def action_call_fold(call_amount):
        def player_call_fold(amount):
            player_call_fold.times_called += 1
            if player_call_fold.times_called > call_amount:
                return Action.ACTION_FOLD, 0
            return Action.ACTION_CALL, amount

        player_call_fold.times_called = 0
        return player_call_fold

    @staticmethod
    def action_check_call():
        def player_action_call(amount):
            return Action.ACTION_CALL, amount

        return player_action_call

    @staticmethod
    def action_fold():

        def player_action_raise(_):
            player_action_raise.times_called += 1
            if player_action_raise.times_called > 1:
                raise Exception("Player not expected to be asked for actions after folding")
            return Action.ACTION_FOLD, 0

        player_action_raise.times_called = 0
        return player_action_raise

    @staticmethod
    def action_raise(new_required_total_player_contribution_to_pot):
        def player_action_raise(amount):
            return Action.ACTION_RAISE, new_required_total_player_contribution_to_pot

        return player_action_raise

    def action_raise_call(self, new_required_total_player_contribution_to_pot):
        def raise_call(amount):
            if amount < new_required_total_player_contribution_to_pot:
                return Action.ACTION_RAISE, new_required_total_player_contribution_to_pot
            return Action.ACTION_CALL, amount

        return raise_call

    def action_raise_reraise(self, raise_amount):
        def raise_reraise(amount):
            return Action.ACTION_RAISE, amount + raise_amount

        return raise_reraise

    def action_bet_fold(self, new_required_total_player_contribution_to_pot):
        def raise_fold(amount):
            if amount < new_required_total_player_contribution_to_pot:
                return Action.ACTION_RAISE, new_required_total_player_contribution_to_pot
            return Action.ACTION_FOLD, 0

        return raise_fold

    def test_deal(self):
        player1 = Player("player1", 1000)
        player2 = Player("player2", 1000)
        seating = Seating([player1, player2])
        deck = Deck()
        deck.initialize()
        dealer = Dealer(deck, seating)
        dealer.deal_cards_to_players()
        hand_size = 2
        cards_dealt = len(seating.players) * hand_size
        self.assertEqual(cards_dealt, len(set(player1.cards + player2.cards)))
        expected_remaining_card_count = TestDeck.deck_size - cards_dealt
        self.assertEqual(expected_remaining_card_count, len(deck.cards))

    def test_collect_blinds(self):
        initial_stack = 1000
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        button_player = self.setup_new_player("Button", initial_stack)
        player2 = self.setup_new_player("SmallBlind", initial_stack)
        player3 = self.setup_new_player("BigBlind", initial_stack)
        seating = Seating([button_player, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.pot = Pot()
        dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack, button_player.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size, player3.stack)
        self.assertEqual(big_blind_size + small_blind_size, dealer.pot.total_count())
        dealer.move_button()
        dealer.pot = Pot()
        dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack - big_blind_size, button_player.stack)
        self.assertEqual(initial_stack - small_blind_size, player2.stack)
        self.assertEqual(initial_stack - big_blind_size - small_blind_size, player3.stack)
        self.assertEqual(big_blind_size + small_blind_size, dealer.pot.total_count())
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)

    def test_collect_blinds__when_player_dont_have_enough_chips(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        button_player = self.setup_new_player("Button", 100)
        player2 = self.setup_new_player("SmallBlind", small_blind_size - 1)
        player3 = self.setup_new_player("BigBlind", big_blind_size - 1)
        seating = Seating([button_player, player2, player3])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.pot = Pot()
        dealer.collect_blinds(small_blind_size)
        self.assertEqual(initial_stack, button_player.stack)
        self.assertEqual(0, player2.stack)
        self.assertEqual(0, player3.stack)
        self.assertEqual(13, dealer.pot.total_count())
        self.assertTrue(player2 in dealer.pot.players)
        self.assertTrue(player3 in dealer.pot.players)

    def test_move_button__when2players(self):
        initial_button_player = self.setup_new_player("Button", 100)
        initial_bb_player = self.setup_new_player("BigBlind", 100)
        seating = Seating([initial_button_player, initial_bb_player])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.move_button()
        seating.button_pos = 0
        dealer.move_button()
        seating.button_pos = 1
        dealer.move_button()
        seating.button_pos = 0

    def test_move_button__when5players(self):
        player1 = self.setup_new_player("Player1", 100)
        player2 = self.setup_new_player("Player2", 100)
        initial_button_player = self.setup_new_player("Button", 100)
        initial_sb_player = self.setup_new_player("SmallBlind", 100)
        initial_bb_player = self.setup_new_player("BigBlind", 100)
        seating = Seating([player1, player2, initial_button_player, initial_sb_player, initial_bb_player])
        deck = Deck()
        dealer = Dealer(deck, seating)
        dealer.move_button()
        seating.button_pos = 0
        dealer.move_button()
        seating.button_pos = 1
        dealer.move_button()
        seating.button_pos = 2
        dealer.move_button()
        seating.button_pos = 3
        dealer.move_button()
        seating.button_pos = 4
        dealer.move_button()
        seating.button_pos = 5
        dealer.move_button()
        seating.button_pos = 0

    def test_preflop_round__when_all_fold(self):
        initial_stack = 1000
        small_blind_size = 15
        dealer = self.setup_3_player_preflop_where_everybody_folds(initial_stack)
        button_player = dealer.seating.players[0]
        sb_player = dealer.seating.players[1]
        bb_player = dealer.seating.players[2]
        winner = dealer.play_preflop(small_blind_size)
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack + small_blind_size, bb_player.stack)
        self.assertEqual(initial_stack, button_player.stack)
        self.assertEqual(initial_stack - small_blind_size, sb_player.stack)

    def test_preflop_round__when_only_small_blind_plays(self):
        initial_stack = 100
        small_blind_size = 5
        dealer = self.setup_3_player_preflop_where_everybody_folds(initial_stack)
        button_player = dealer.seating.players[0]
        sb_player = dealer.seating.players[1]
        bb_player = dealer.seating.players[2]
        sb_player.act = self.action_check_call()
        winner = dealer.play_preflop(small_blind_size)
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack + small_blind_size * 2, sb_player.stack)
        self.assertEqual(initial_stack, button_player.stack)
        self.assertEqual(initial_stack - small_blind_size * 2, bb_player.stack)

    def setup_3_player_preflop_where_everybody_folds(self, initial_stack):
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        button_player.act = self.action_fold()
        sb_player.act = self.action_fold()
        bb_player.act = self.action_fold()
        seating = Seating([button_player, sb_player, bb_player])
        dealer = Dealer(None, seating)
        dealer.setup_deck()
        return dealer

    def test_preflop_round__when_only_button_plays(self):
        initial_stack = 100
        small_blind_size = 5
        dealer = self.setup_3_player_preflop_where_everybody_folds(initial_stack)
        button_player = dealer.seating.players[0]
        sb_player = dealer.seating.players[1]
        bb_player = dealer.seating.players[2]
        button_player.act = self.action_check_call()
        winner = dealer.play_preflop(small_blind_size)
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack + small_blind_size * 3, button_player.stack)
        self.assertEqual(initial_stack - small_blind_size, sb_player.stack)
        self.assertEqual(initial_stack - small_blind_size * 2, bb_player.stack)

    def test_preflop_round__when_all_calls(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        dealer = self.setup_3_player_preflop_where_everybody_folds(initial_stack)
        button_player = dealer.seating.players[0]
        sb_player = dealer.seating.players[1]
        bb_player = dealer.seating.players[2]
        button_player.act = self.action_check_call()
        sb_player.act = self.action_check_call()
        bb_player.act = self.action_check_call()
        winner = dealer.play_preflop(small_blind_size)
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player in dealer.pot.players)
        self.assertEqual(initial_stack - big_blind_size, button_player.stack)
        self.assertEqual(initial_stack - big_blind_size, sb_player.stack)
        self.assertEqual(initial_stack - big_blind_size, bb_player.stack)
        self.assertEqual(big_blind_size * 3, dealer.pot.total_count())

    def test_preflop_round__when_all_calls__correct_state_of_cards_dealt(self):
        initial_stack = 100
        small_blind_size = 5
        dealer = self.setup_3_player_preflop_where_everybody_folds(initial_stack)
        button_player = dealer.seating.players[0]
        sb_player = dealer.seating.players[1]
        bb_player = dealer.seating.players[2]
        button_player.act = self.action_check_call()
        sb_player.act = self.action_check_call()
        bb_player.act = self.action_check_call()
        dealer.play_preflop(small_blind_size)
        self.assertEqual(0, len(dealer.community_cards))
        self.assertEqual(TestDeck.deck_size - len(dealer.seating.players) * 2, len(dealer.deck.cards))
        self.assertEqual(2, len(button_player.cards))
        self.assertEqual(2, len(sb_player.cards))
        self.assertEqual(2, len(bb_player.cards))

    def test_preflop_round__when_player_bets__all_calls(self):
        initial_stack = 100
        bet_size = 50
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        button_player.act = self.action_check_call()
        sb_player.act = self.action_raise(bet_size)
        bb_player.act = self.action_check_call()
        seating = Seating([button_player, sb_player, bb_player])
        dealer = Dealer(None, seating)
        dealer.setup_deck()
        winner = dealer.play_preflop(small_blind_size)
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size, button_player.stack)
        self.assertEqual(initial_stack - bet_size, sb_player.stack)
        self.assertEqual(initial_stack - bet_size, bb_player.stack)
        self.assertEqual(bet_size * 3, dealer.pot.total_count())

    def test_preflop_round__when_first_player_bets__all_calls(self):
        initial_stack = 100
        bet_size = 50
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        button_player.act = self.action_raise(bet_size)
        sb_player.act = self.action_check_call()
        bb_player.act = self.action_check_call()
        seating = Seating([button_player, sb_player, bb_player])
        dealer = Dealer(None, seating)
        dealer.setup_deck()
        winner = dealer.play_preflop(small_blind_size)
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size, button_player.stack)
        self.assertEqual(initial_stack - bet_size, sb_player.stack)
        self.assertEqual(initial_stack - bet_size, bb_player.stack)
        self.assertEqual(bet_size * 3, dealer.pot.total_count())

    def test_preflop_round__when_player_raises__all_calls(self):
        initial_stack = 100
        bet_size = 50
        raise_size = bet_size + 10
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)

        def call_raise(player_name):
            def call_raise_action(amount):
                if amount == small_blind_size * 2:
                    print(player_name + " calls " + str(amount))
                    return Action.ACTION_CALL, amount
                print(player_name + " raises to " + str(raise_size))
                return Action.ACTION_RAISE, raise_size

            return call_raise_action

        button_player.act = call_raise("Button")

        def raise_call(player_name):
            def raise_call_action(amount):
                if amount == small_blind_size * 2:
                    print(player_name + " raises to " + str(bet_size))
                    return Action.ACTION_RAISE, bet_size
                print(player_name + " calls " + str(amount))
                return Action.ACTION_CALL, amount

            return raise_call_action

        sb_player.act = raise_call("SmallBlind")
        bb_player.act = self.action_check_call()
        seating = Seating([button_player, sb_player, bb_player])
        dealer = Dealer(None, seating)
        dealer.setup_deck()
        winner = dealer.play_preflop(small_blind_size)
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player in dealer.pot.players)
        self.assertEqual(initial_stack - raise_size, button_player.stack)
        self.assertEqual(initial_stack - raise_size, sb_player.stack)
        self.assertEqual(initial_stack - raise_size, bb_player.stack)
        self.assertEqual(raise_size * 3, dealer.pot.total_count())

    def test_playing_flop__when_all_fold__button_player_wins(self):
        initial_stack = 100
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        button_player.act = self.action_fold()
        sb_player.act = self.action_fold()
        bb_player.act = self.action_fold()
        winner = dealer.play_flop()
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack + small_blind_size * 4, button_player.stack)

    def test_playing_flop__when_bb_checks_and_others_fold__bb_player_wins(self):
        initial_stack = 100
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        button_player.act = self.action_fold()
        sb_player.act = self.action_fold()
        bb_player.act = self.action_check_call()
        winner = dealer.play_flop()
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack + small_blind_size * 4, bb_player.stack)

    def test_playing_flop__when_all_checks(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind = small_blind_size * 2
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        winner = dealer.play_flop()
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player in dealer.pot.players)
        self.assertEqual(initial_stack - big_blind, button_player.stack)
        self.assertEqual(initial_stack - big_blind, sb_player.stack)
        self.assertEqual(initial_stack - big_blind, bb_player.stack)
        self.assertEqual(big_blind * 3, dealer.pot.total_count())

    def test_playing_flop__when_all_checks__cards_dealt_correctly(self):
        initial_stack = 100
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        dealer.play_flop()
        self.assertEqual(3, len(dealer.community_cards))
        self.assertEqual(TestDeck.deck_size - len(players) * 2 - 3, len(dealer.deck.cards))

    def test_playing_flop__when_small_blind_is_10_and_player_bets__2players_calls(self):
        self.execute_test_of_player_betting_post_flop_and_all_calling(10, 3)

    def test_playing_flop__when_small_blind_is_15_and_player_bets__2players_calls(self):
        self.execute_test_of_player_betting_post_flop_and_all_calling(15, 3)

    def test_playing_flop__when_small_blind_is_15_and_player_bets__4players_calls(self):
        self.execute_test_of_player_betting_post_flop_and_all_calling(15, 5)

    def execute_test_of_player_betting_post_flop_and_all_calling(self, small_blind_size, player_count):
        initial_stack = 100
        big_blind_size = small_blind_size * 2
        bet_size = big_blind_size + 20
        players = [self.setup_new_player("Player" + str(i), initial_stack) for i in range(player_count)]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)
        players[player_count - 1].act = self.action_raise(bet_size)
        winner = dealer.play_flop()
        self.assertEqual(False, winner)
        self.assertTrue(all(p in dealer.pot.players for p in players))
        self.assertTrue(all(p.stack == initial_stack - bet_size for p in players))
        self.assertEqual(bet_size * player_count, dealer.pot.total_count())

    def test_playing_flop__when_player_bets_20__one_folds_another_calls(self):
        self.execute_test_of_player_betting_post_flop(20)

    # todo can this be made into test case?
    def test_playing_flop__when_player_bets_50__one_folds_another_calls(self):
        self.execute_test_of_player_betting_post_flop(50)

    def execute_test_of_player_betting_post_flop(self, bet_amount):
        initial_stack = 100
        small_blind_size = 10
        big_blind_size = small_blind_size * 2
        bet_size = big_blind_size + bet_amount
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)

        button_player.act = self.action_check_call()
        sb_player.act = self.action_raise(bet_size)
        bb_player.act = self.action_fold()
        winner = dealer.play_flop()
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player not in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size, button_player.stack)
        self.assertEqual(initial_stack - bet_size, sb_player.stack)
        self.assertEqual(initial_stack - big_blind_size, bb_player.stack)
        self.assertEqual(bet_size * 2 + big_blind_size, dealer.pot.total_count())

    def test_playing_flop_when_player_raises_and_is_called_by_original_betting_player(self):
        initial_stack = 100
        small_blind_size = 10
        big_blind_size = small_blind_size * 2
        bet_size = big_blind_size + 30
        raise_size = bet_size + 20
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)

        button_player.act = self.action_raise(raise_size)
        sb_player.act = self.action_raise_call(bet_size)
        bb_player.act = self.action_fold()
        winner = dealer.play_flop()
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player not in dealer.pot.players)
        self.assertEqual(initial_stack - raise_size, button_player.stack)
        self.assertEqual(initial_stack - raise_size, sb_player.stack)
        self.assertEqual(initial_stack - big_blind_size, bb_player.stack)
        self.assertEqual(raise_size * 2 + big_blind_size, dealer.pot.total_count())

    def test_playing_flop_when_player_raises_and_is_reraised_by_original_betting_player(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        bet_size = 40
        raise_size = 20
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)

        button_player.act = self.action_raise_call(bet_size)
        sb_player.act = self.action_raise_reraise(raise_size)
        bb_player.act = self.action_fold()
        winner = dealer.play_flop()
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player not in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size - raise_size, button_player.stack)
        self.assertEqual(initial_stack - bet_size - raise_size, sb_player.stack)
        self.assertEqual(initial_stack - big_blind_size, bb_player.stack)
        self.assertEqual(raise_size * 2 + bet_size * 2 + big_blind_size, dealer.pot.total_count())

    def test_playing_flop_when_player_raises_and_original_betting_player_folds(self):
        initial_stack = 100
        small_blind_size = 10
        big_blind_size = small_blind_size * 2
        bet_size = big_blind_size + 30
        raise_size = bet_size + 20
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)

        button_player.act = self.action_raise(raise_size)
        sb_player.act = self.action_bet_fold(bet_size)
        bb_player.act = self.action_fold()
        winner = dealer.play_flop()
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack - bet_size, sb_player.stack)
        self.assertEqual(initial_stack + bet_size + big_blind_size, button_player.stack)
        self.assertEqual(initial_stack - big_blind_size, bb_player.stack)

    def test_playing_flop_players_are_asked_for_actions_in_correct_order_starting_sb_player(self):
        order_of_calls = []

        def action_raise_call_and_register_order(player_name, new_required_total_player_contribution_to_pot):
            def raise_call(amount):
                order_of_calls.append(player_name)
                if amount < new_required_total_player_contribution_to_pot:
                    print(player_name + " raises to " + str(new_required_total_player_contribution_to_pot))
                    return Action.ACTION_RAISE, new_required_total_player_contribution_to_pot
                print(player_name + " calls " + str(amount))
                return Action.ACTION_CALL, amount

            return raise_call

        initial_stack = 1000
        small_blind_size = 10
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_preflop_where_everybody_calls(players, small_blind_size)

        button_player.act = action_raise_call_and_register_order("Button", 100)
        sb_player.act = action_raise_call_and_register_order("SmallBlind", 40)
        bb_player.act = action_raise_call_and_register_order("BigBlind", 60)

        dealer.play_flop()
        self.assertEqual("SmallBlind", order_of_calls[0])
        self.assertEqual("BigBlind", order_of_calls[1])
        self.assertEqual("Button", order_of_calls[2])
        self.assertEqual("SmallBlind", order_of_calls[3])
        self.assertEqual("BigBlind", order_of_calls[4])

    def setup_dealer_and_play_preflop_where_everybody_calls(self, players, small_blind_size):
        for player in players:
            player.act = self.action_check_call()
        seating = Seating(players)
        dealer = Dealer(None, seating)
        dealer.setup_deck()
        winner = dealer.play_preflop(small_blind_size)
        print("# Preflop concluded")
        self.assertEqual(False, winner)
        return dealer

    def setup_dealer_and_play_flop_where_everybody_calls(self, players, small_blind_size):
        for player in players:
            player.act = self.action_check_call()
        seating = Seating(players)
        dealer = Dealer(None, seating)
        dealer.setup_deck()
        winner = dealer.play_preflop(small_blind_size)
        print("# Preflop concluded")
        self.assertEqual(False, winner)
        winner = dealer.play_flop()
        print("# Flop concluded")
        self.assertEqual(False, winner)
        return dealer

    def setup_dealer_and_play_turn_where_everybody_calls(self, players, small_blind_size,
                                                         random_seed_for_shuffling=None):
        for player in players:
            player.act = self.action_check_call()
        seating = Seating(players)
        dealer = Dealer(None, seating, random_seed_for_shuffling)
        dealer.setup_deck()
        winner = dealer.play_preflop(small_blind_size)
        print("# Preflop concluded")
        self.assertEqual(False, winner)
        winner = dealer.play_flop()
        print("# Flop concluded")
        self.assertEqual(False, winner)
        winner = dealer.play_turn()
        print("# Turn concluded")
        self.assertEqual(False, winner)
        return dealer

    def test_playing_turn__when_all_fold__button_player_wins(self):
        initial_stack = 100
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_flop_where_everybody_calls(players, small_blind_size)
        button_player.act = self.action_fold()
        sb_player.act = self.action_fold()
        bb_player.act = self.action_fold()
        winner = dealer.play_turn()
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack + small_blind_size * 4, button_player.stack)

    def test_playing_turn__when_all_checks(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind = small_blind_size * 2
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_flop_where_everybody_calls(players, small_blind_size)
        winner = dealer.play_turn()
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player in dealer.pot.players)
        self.assertEqual(initial_stack - big_blind, button_player.stack)
        self.assertEqual(initial_stack - big_blind, sb_player.stack)
        self.assertEqual(initial_stack - big_blind, bb_player.stack)
        self.assertEqual(big_blind * 3, dealer.pot.total_count())

    def test_playing_turn__when_all_checks__cards_dealt_correctly(self):
        initial_stack = 100
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_flop_where_everybody_calls(players, small_blind_size)
        dealer.play_turn()
        self.assertEqual(4, len(dealer.community_cards))
        self.assertEqual(TestDeck.deck_size - len(players) * 2 - 4, len(dealer.deck.cards))

    def test_playing_turn_when_player_raises_and_is_reraised_by_original_betting_player(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        bet_size = 40
        raise_size = 20
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_flop_where_everybody_calls(players, small_blind_size)

        button_player.act = self.action_raise_call(bet_size)
        sb_player.act = self.action_raise_reraise(raise_size)
        bb_player.act = self.action_fold()
        winner = dealer.play_turn()
        self.assertEqual(False, winner)
        self.assertTrue(button_player in dealer.pot.players)
        self.assertTrue(sb_player in dealer.pot.players)
        self.assertTrue(bb_player not in dealer.pot.players)
        self.assertEqual(initial_stack - bet_size - raise_size, button_player.stack)
        self.assertEqual(initial_stack - bet_size - raise_size, sb_player.stack)
        self.assertEqual(initial_stack - big_blind_size, bb_player.stack)
        self.assertEqual(raise_size * 2 + bet_size * 2 + big_blind_size, dealer.pot.total_count())

    def test_playing_river__when_all_fold__button_player_wins(self):
        initial_stack = 100
        small_blind_size = 5
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_turn_where_everybody_calls(players, small_blind_size)
        button_player.act = self.action_fold()
        sb_player.act = self.action_fold()
        bb_player.act = self.action_fold()
        winner = dealer.play_river()
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack + small_blind_size * 4, button_player.stack)

    def test_playing_river_when_player_raises_and_original_betting_player_folds(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind_size = small_blind_size * 2
        bet_size = big_blind_size + 30
        raise_size = bet_size + 20
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        dealer = self.setup_dealer_and_play_turn_where_everybody_calls(players, small_blind_size)

        button_player.act = self.action_raise(raise_size)
        sb_player.act = self.action_bet_fold(bet_size)
        bb_player.act = self.action_fold()
        winner = dealer.play_river()
        self.assertEqual(True, winner)
        self.assertEqual(initial_stack - bet_size, sb_player.stack)
        self.assertEqual(initial_stack + bet_size + big_blind_size, button_player.stack)
        self.assertEqual(initial_stack - big_blind_size, bb_player.stack)

    def test_playing_river__when_all_checks__player_with_best_hand_wins1(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind = small_blind_size * 2
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        random_seed_for_shuffling = 4
        # seed value 4 results in shuffling where Button has a high card, SmallBlind with Flush, BigBlind with a Pair.
        dealer = self.setup_dealer_and_play_turn_where_everybody_calls(players, small_blind_size,
                                                                       random_seed_for_shuffling)
        dealer.play_river()
        self.assertEqual(initial_stack + big_blind * 2, sb_player.stack)
        self.assertEqual(initial_stack - big_blind, button_player.stack)
        self.assertEqual(initial_stack - big_blind, bb_player.stack)

    def test_playing_river__when_all_checks__player_with_best_hand_wins2(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind = small_blind_size * 2
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        random_seed_for_shuffling = 2
        # seed value 2 results in shuffling where Button has a Pair, SmallBlind with High Card, BigBlind with a Pair, but BigBlind has a better 2nd kicker
        dealer = self.setup_dealer_and_play_turn_where_everybody_calls(players, small_blind_size,
                                                                       random_seed_for_shuffling)
        dealer.play_river()
        self.assertEqual(initial_stack + big_blind * 2, bb_player.stack)
        self.assertEqual(initial_stack - big_blind, sb_player.stack)
        self.assertEqual(initial_stack - big_blind, button_player.stack)

    def test_playing_river__when_only_players_in_pot_participate_in_showdown(self):
        initial_stack = 100
        small_blind_size = 5
        big_blind = small_blind_size * 2
        button_player = self.setup_new_player("Button", initial_stack)
        sb_player = self.setup_new_player("SmallBlind", initial_stack)
        bb_player = self.setup_new_player("BigBlind", initial_stack)
        players = [button_player, sb_player, bb_player]
        random_seed_for_shuffling = 2
        # seed value 2 results in shuffling where Button has a Pair, SmallBlind with High Card, BigBlind with a Pair, but BigBlind has a better 2nd kicker
        dealer = self.setup_dealer_and_play_turn_where_everybody_calls(players, small_blind_size,
                                                                       random_seed_for_shuffling)
        bb_player.act = self.action_fold()
        winner = dealer.play_river()
        self.assertEqual(initial_stack + big_blind * 2, button_player.stack)
        self.assertEqual(initial_stack - big_blind, sb_player.stack)
        self.assertEqual(initial_stack - big_blind, bb_player.stack)
