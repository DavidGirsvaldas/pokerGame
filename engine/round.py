class Round:

    def __init__(self, dealer):
        self.dealer = dealer

    def play_round(self, small_blind):
        self.dealer.setup_deck()
        winner = self.dealer.play_preflop(small_blind)
        if winner:
            self.dealer.move_button()
            return winner
        print("# Preflop concluded")
        winner = self.dealer.play_flop()
        if winner:
            self.dealer.move_button()
            return winner
        print("# Flop concluded")
        winner = self.dealer.play_turn()
        if winner:
            self.dealer.move_button()
            return winner
        print("# Turn concluded")
        self.dealer.move_button()
        return self.dealer.play_river()

