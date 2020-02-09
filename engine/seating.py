class Seating:

    def __init__(self, players):
        self.players = players
        self.button_pos = 0

    def small_blind_player(self):
        return self.players[self.button_pos + 1]

    def big_blind_player(self):
        if self.button_pos == len(self.players) - 2:
            return self.players[0]
        return self.players[self.button_pos + 2]
