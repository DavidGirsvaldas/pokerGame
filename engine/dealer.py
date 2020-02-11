from engine.action import Action
from engine.deck import Deck
from engine.pot import Pot


class Dealer:

    def __init__(self, deck, seating):
        self.community_cards = None
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
        available_size_of_big_blind = min(small_blind_size * 2, bb_player.stack)
        sb_player.stack -= available_size_of_small_blind
        sb_player.money_in_pot = available_size_of_small_blind
        bb_player.stack -= available_size_of_big_blind
        bb_player.money_in_pot = available_size_of_big_blind
        return Pot(available_size_of_small_blind + available_size_of_big_blind, [sb_player, bb_player])

    def setup_preflop(self, small_blind_size):
        self.pot = self.collect_blinds(small_blind_size)
        self.deck = Deck()
        self.deck.initialize()
        self.deck.shuffle()
        self.deal()

    def preflop_round(self, small_blind_size):
        def conclude_preflop(winner):
            if winner:
                winner = self.pot.players[0]
                winner.stack += self.pot.size
                return winner
            else:
                self.community_cards = self.deck.draw(3)

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
                    current_player.stack -= amount_to_add
                    current_player.money_in_pot += amount_to_add
                    self.pot.size += amount_to_add
                    if current_player not in self.pot.players:
                        self.pot.players.append(current_player)
                if player_action is Action.ACTION_RAISE:
                    amount_to_add = new_amount_to_call - current_player.money_in_pot
                    current_player.stack -= amount_to_add
                    current_player.money_in_pot += amount_to_add
                    self.pot.size += amount_to_add
                    if current_player not in self.pot.players:
                        self.pot.players.append(current_player)
                    return round_of_calls_to_make(current_player, False, new_amount_to_call)
                if len(self.pot.players) == 1:
                    return conclude_preflop(self.pot.players[0])
                if current_player is starting_player:
                    return conclude_preflop(None)
                current_player = self.seating.next_player_after_player(current_player)
                if current_player is starting_player and not include_starting_player:
                    return conclude_preflop(None)


        return round_of_calls_to_make(bb_player, True, amount_to_match)
