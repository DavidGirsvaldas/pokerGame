class Player:
    def __init__(self, name, initial_stack = 0):
        self.cards = []
        self.stack = initial_stack
        self.money_in_pot = 0
        self.name = name

    def receive_cards(self, cards):
        self.cards = cards

    def release_cards(self):
        self.cards.clear()

    def __str__(self):
        return self.name + " (" + str(self.stack)+ ")"


