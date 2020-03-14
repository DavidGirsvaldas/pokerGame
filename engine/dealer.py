from engine import card_showdown
from engine.action import Action
from engine.deck import Deck
from engine.pot import Pot


class Dealer:

    def __init__(self, deck, seating, random_seed_for_shuffling=None):
        self.community_cards = []
        self.deck = deck
        self.seating = seating
        self.pot = None
        self.big_blind_size = None
        self.random_seed_for_shuffling = random_seed_for_shuffling

    def deal_cards_to_players(self):
        for player in self.seating.players:
            player.receive_cards(self.deck.draw(2))

    def move_button(self):
        self.seating.move_button()

    def collect_blinds(self, small_blind_size):
        for player in self.seating.players:
            player.money_in_pot = 0
        sb_player = self.seating.small_blind_player()
        bb_player = self.seating.big_blind_player()
        available_size_of_small_blind = min(small_blind_size, sb_player.stack)
        self.pot.player_calls(sb_player, available_size_of_small_blind)
        available_size_of_big_blind = min(small_blind_size * 2, bb_player.stack)
        self.pot.player_calls(bb_player, available_size_of_big_blind)

    def setup_deck(self):
        self.deck = Deck()
        self.deck.initialize()
        self.deck.shuffle(self.random_seed_for_shuffling)

    def add_community_cards(self, card_count):
        self.community_cards += self.deck.draw(card_count)
        print("Community cards: " + ", ".join([str(card) for card in self.community_cards]))

    def play_preflop(self, small_blind_size):
        self.big_blind_size = small_blind_size * 2
        self.pot = Pot()
        self.collect_blinds(small_blind_size)
        self.deal_cards_to_players()
        bb_player = self.seating.big_blind_player()
        amount_to_match = small_blind_size * 2
        return self.ask_players_for_actions(bb_player, amount_to_match, True)

    def play_flop(self):
        self.add_community_cards(3)
        last_player_to_go = self.seating.button_player()
        return self.ask_players_for_actions(last_player_to_go, last_player_to_go.money_in_pot, True)

    def play_turn(self):
        self.add_community_cards(1)
        last_player_to_go = self.seating.button_player()
        return self.ask_players_for_actions(last_player_to_go, last_player_to_go.money_in_pot, True)

    def play_river(self):
        self.add_community_cards(1)
        last_player_to_go = self.seating.button_player()
        winner = self.ask_players_for_actions(last_player_to_go, last_player_to_go.money_in_pot, True)
        if winner:
            return True
        else:
            for pot in self.pot.get_all_pots():
                winners = card_showdown.find_winners(pot.players, self.community_cards)
                players_share = int(pot.pot_size() / len(winners))
                for player in winners:
                    player.stack += players_share

    def ask_players_for_actions(self, player_who_raised, new_raised_amount, include_last_player):
        next_player = self.seating.next_player_after_player(player_who_raised)
        amount_of_calls_to_make = len(self.seating.players)
        if not include_last_player:
            amount_of_calls_to_make -= 1
        for i in range(amount_of_calls_to_make):
            if next_player.cards and next_player.stack > 0:
                p_action, p_amount = next_player.act(new_raised_amount)
                if p_action == Action.ACTION_FOLD:
                    print(str(next_player) + " folds")
                    self.player_folds(next_player)
                elif p_action == Action.ACTION_CALL:
                    print(str(next_player) + " calls " + str(p_amount))
                    self.pot.player_calls(next_player, p_amount)
                elif p_action == Action.ACTION_RAISE:
                    print(str(next_player) + " raises to " + str(p_amount))
                    self.pot.player_calls(next_player, p_amount)
                    return self.ask_players_for_actions(next_player, p_amount, False)
                if self.is_winner_determined():
                    winner = list(self.pot.players.keys())[0]
                    winner.stack += self.pot.pot_size()
                    return True
            next_player = self.seating.next_player_after_player(next_player)
        return False

    def is_winner_determined(self):
        return len(self.pot.players) == 1

    def player_folds(self, player):
        player.money_in_pot = 0
        player.cards = None
        if player in self.pot.players:
            self.pot.size += self.pot.players[player]
            self.pot.players.pop(player, None)
