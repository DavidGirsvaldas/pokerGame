class Round:

    def __init__(self, dealer):
        self.dealer = dealer

    def play_round(self):
        self.dealer.setup_deck()
        winner = self.dealer.play_preflop(5) # todo remove assumption small blind always 5
        if winner:
            return winner
        print("# Preflop concluded")
        winner = self.dealer.play_flop()
        if winner:
            return winner
        print("# Flop concluded")
        winner = self.dealer.play_turn()
        if winner:
            return winner
        print("# Turn concluded")
        self.dealer.move_button()
        print("# River concluded")
        return self.dealer.play_river()
