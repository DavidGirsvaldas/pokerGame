from engine.action import Action
from engine.deck import Deck
from engine.pot import Pot


class Dealer:

    def __init__(self, deck, seating):
        self.community_cards = []
        self.deck = deck
        self.seating = seating
        self.pot = None

    def deal(self):
        for player in self.seating.players:
            player.cards = self.deck.draw(2)

    def move_button(self):
        if self.seating.button_pos == len(self.seating.players) - 1:
            self.seating.button_pos = 0
            return
        self.seating.button_pos += 1

    def collect_blinds(self, small_blind_size):
        sb_player = self.seating.small_blind_player()
        bb_player = self.seating.big_blind_player()
        available_size_of_small_blind = min(small_blind_size, sb_player.stack)
        self.take_chips(sb_player, available_size_of_small_blind)
        available_size_of_big_blind = min(small_blind_size * 2, bb_player.stack)
        self.take_chips(bb_player, available_size_of_big_blind)

    def setup_preflop(self, small_blind_size):
        self.pot = Pot()
        self.collect_blinds(small_blind_size)
        self.deck = Deck()
        self.deck.initialize()
        self.deck.shuffle()
        self.deal()

    def add_community_cards(self, card_count):
        self.community_cards += self.deck.draw(card_count)

    def take_chips(self, player, amount):
        player.stack -= amount
        player.money_in_pot += amount
        self.pot.size += amount
        if player not in self.pot.players:
            self.pot.players.append(player)

    def preflop_round(self, small_blind_size):
        bb_player = self.seating.big_blind_player()
        amount_to_match = small_blind_size * 2

        def round_of_calls_to_make(starting_player, include_starting_player, chips_in_pot_per_player):
            current_player = self.seating.next_player_after_player(starting_player)
            while True:
                player_action, new_amount_to_call = current_player.act(chips_in_pot_per_player)
                if player_action is Action.ACTION_FOLD:
                    self.player_folds(current_player)
                if player_action is Action.ACTION_CALL:
                    amount_to_add = new_amount_to_call - current_player.money_in_pot
                    self.take_chips(current_player, amount_to_add)
                if player_action is Action.ACTION_RAISE:
                    amount_to_add = new_amount_to_call - current_player.money_in_pot
                    self.take_chips(current_player, amount_to_add)
                    return round_of_calls_to_make(current_player, False, new_amount_to_call)
                if self.is_winner_determined():
                    return self.award_winner()
                if current_player is starting_player:
                    self.add_community_cards(3)
                    return
                current_player = self.seating.next_player_after_player(current_player)
                if current_player is starting_player and not include_starting_player:
                    self.add_community_cards(3)
                    return

        return round_of_calls_to_make(bb_player, True, amount_to_match)

    def play_flop(self):
        def ask_players_for_actions(player_who_raised, new_raised_amount):
            next_player = self.seating.next_player_after_player(player_who_raised)
            for i in range(len(self.seating.players)-1):
                p_action, p_amount = next_player.act(new_raised_amount)
                if p_action == Action.ACTION_FOLD:
                    self.player_folds(next_player)
                elif p_action == Action.ACTION_CALL:
                    self.player_calls(next_player, p_amount)
                elif p_action == Action.ACTION_RAISE:
                    self.player_calls(next_player, p_amount)
                    return ask_players_for_actions(next_player, p_amount)
                if self.is_winner_determined():
                    return self.award_winner()
                next_player = self.seating.next_player_after_player(next_player)

        self.add_community_cards(1)  # todo should be revealed at the end, not start
        last_player_to_go = self.seating.players[0]  # todo remove assumption that button sits at position 0
        player = self.seating.next_player_after_player(last_player_to_go)
        for i in range(len(self.pot.players)):
            action, amount = player.act(0)
            if action == Action.ACTION_FOLD:
                self.player_folds(player)
            if action == Action.ACTION_RAISE:
                self.player_calls(player, amount)
                return ask_players_for_actions(player, amount)
            if self.is_winner_determined():
                return self.award_winner()
            player = self.seating.next_player_after_player(player)

    def player_calls(self, player, amount):
        player.stack -= amount - player.money_in_pot
        self.pot.size += amount - player.money_in_pot
        player.money_in_pot += amount - player.money_in_pot

    def is_winner_determined(self):
        return len(self.pot.players) == 1

    def award_winner(self):
        winner = self.pot.players[0]
        winner.stack += self.pot.size
        return winner

    def player_folds(self, player):
        player.money_in_pot = 0
        if player in self.pot.players:
            self.pot.players.remove(player)
