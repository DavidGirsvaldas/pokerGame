class Player:

    def __init__(self, initial_stack = 0):
        self.cards = []
        self.stack = initial_stack
        self.money_in_pot = 0

    def receive_cards(self, cards):
        self.cards = cards


