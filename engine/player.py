class Player:
    def __init__(self, name, initial_stack = 0):
        self.cards = []
        self.stack = initial_stack
        self.money_in_pot = 0
        self.name = name
        self.community_cards = []

    def receive_cards(self, cards):
        self.cards = cards

    def release_cards(self):
        self.cards.clear()
        self.community_cards = []

    def see_community_cards(self, cards):
        self.community_cards = cards

    def __str__(self):
        return self.name + " (" + str(self.stack)+ ")"


