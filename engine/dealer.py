class Dealer():

    def __init__(self, deck, players):
        self.deck = deck
        self.players = players

    def deal(self):
        for player in self.players:
            player.receive_cards(self.deck.draw(2))
