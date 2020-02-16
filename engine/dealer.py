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
        def conclude_preflop(winner):
            if winner:
                winner = self.pot.players[0]
                winner.stack += self.pot.size
                return winner
            else:
                self.add_community_cards(3)

        bb_player = self.seating.big_blind_player()
        amount_to_match = small_blind_size * 2

        def round_of_calls_to_make(starting_player, include_starting_player, chips_in_pot_per_player):
            current_player = self.seating.next_player_after_player(starting_player)
            while True:
                player_action, new_amount_to_call = current_player.act(chips_in_pot_per_player)
                if player_action is Action.ACTION_FOLD:
                    if current_player in self.pot.players:
                        self.pot.players.remove(current_player)
                if player_action is Action.ACTION_CALL:
                    amount_to_add = new_amount_to_call - current_player.money_in_pot
                    self.take_chips(current_player, amount_to_add)
                if player_action is Action.ACTION_RAISE:
                    amount_to_add = new_amount_to_call - current_player.money_in_pot
                    self.take_chips(current_player, amount_to_add)
                    return round_of_calls_to_make(current_player, False, new_amount_to_call)
                if len(self.pot.players) == 1:
                    return conclude_preflop(self.pot.players[0])
                if current_player is starting_player:
                    return conclude_preflop(None)
                current_player = self.seating.next_player_after_player(current_player)
                if current_player is starting_player and not include_starting_player:
                    return conclude_preflop(None)

        return round_of_calls_to_make(bb_player, True, amount_to_match)

    def play_flop(self):
        self.add_community_cards(1)  # todo should be revealed at the end, not start
        last_player_to_go = self.seating.players[0]
        player = last_player_to_go
        for i in range(3):
            player = self.seating.next_player_after_player(player)
            action, amount = player.act(None)
            if action == Action.ACTION_FOLD:
                if player in self.pot.players:
                    self.pot.players.remove(player)
                if len(self.pot.players) == 1:
                    winner = self.pot.players[0]
                    winner.stack += self.pot.size
                    return winner
            if action == Action.ACTION_RAISE:
                player.stack -= amount - 20
                self.pot.size += amount - 20
                for next_player in self.seating.players:
                    if next_player != player:
                        p_action, p_amount = next_player.act(None)
                        if p_action == Action.ACTION_FOLD:
                            self.pot.players.remove(next_player)
                        else:
                            next_player.stack -= amount - 20
                            self.pot.size += amount - 20
                        if len(self.pot.players) == 1:
                            winner = self.pot.players[0]
                            winner.stack += self.pot.size
                            return winner
