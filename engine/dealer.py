class Dealer:

    def __init__(self, deck, seating):
        self.deck = deck
        self.seating = seating

    def deal(self):
        for player in self.seating.players:
            player.receive_cards(self.deck.draw(2))

    def move_button(self):
        if self.seating.button_pos == len(self.seating.players)-1:
            self.seating.button_pos = 0
            return
        self.seating.button_pos += 1
