from engine.deck import Deck
from engine.pot import Pot


class Dealer:

    def __init__(self, deck, seating):
        self.deck = deck
        self.seating = seating
        self.pot = 0

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

    def setup_preflop(self):
        self.pot = self.collect_blinds(5)
        self.deck = Deck()
        self.deck.initialize()
        self.deck.shuffle()
        self.deal()
