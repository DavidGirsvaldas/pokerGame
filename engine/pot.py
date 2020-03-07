class Pot:

    def __init__(self):
        self.size = 0
        self.players = {}

    def total_count(self):
        amount = self.size
        for _, players_chips_in_pot in self.players.items():
            amount += players_chips_in_pot
        return amount

