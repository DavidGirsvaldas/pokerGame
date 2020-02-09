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
        pot = 0
        available_size_of_small_blind = min(small_blind_size, self.seating.small_blind_player().stack)
        available_size_of_big_blind = min(small_blind_size * 2, self.seating.big_blind_player().stack)
        self.seating.small_blind_player().stack -= available_size_of_small_blind
        self.seating.big_blind_player().stack -= available_size_of_big_blind
        return available_size_of_small_blind + available_size_of_big_blind
