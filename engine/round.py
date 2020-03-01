class Round:

    def __init__(self, dealer):
        self.dealer = dealer

    def play_round(self):
        self.dealer.setup_deck()
        # todo return winner when its present
        self.dealer.play_preflop(5) # todo remove assumption small blind always 5
        print("# Preflop concluded")
        self.dealer.play_flop()
        print("# Flop concluded")
        self.dealer.play_turn()
        print("# Turn concluded")
        self.dealer.move_button()
        print("# Flop concluded")
        return self.dealer.play_river()
