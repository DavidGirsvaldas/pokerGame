from engine.action import Action
from engine.deck import Deck
from engine.pot import Pot


class Dealer:

    def __init__(self, deck, seating):
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
        bb_player.stack -= available_size_of_big_blind
        return Pot(available_size_of_small_blind + available_size_of_big_blind, [sb_player, bb_player])

    def setup_preflop(self, small_blind_size):
        self.pot = self.collect_blinds(small_blind_size)
        self.deck = Deck()
        self.deck.initialize()
        self.deck.shuffle()
        self.deal()

    def preflop_round(self):
        bb_player = self.seating.big_blind_player()
        current_player = bb_player
        round_over = False
        while not round_over:
            current_player = self.seating.next_player_after_player(current_player)
            player_action = current_player.act(None)
            if player_action is Action.ACTION_FOLD:
                current_player.cards = None
                if current_player in self.pot.players:
                    self.pot.players.remove(current_player)
                if len(self.pot.players) is 1:
                    winner = self.pot.players[0]
                    winner.stack += self.pot.size
                    return winner
            if player_action is Action.ACTION_CALL:
                if current_player not in self.pot.players:
                    self.pot.players.append(current_player)
            if current_player is bb_player:
                return
