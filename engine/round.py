class Round:

    def __init__(self, dealer):
        self.dealer = dealer

    def play_round(self, small_blind):
        print("# Start round")
        self.dealer.setup_deck()
        is_round_concluded = self.dealer.play_preflop(small_blind)
        if not is_round_concluded:
            print("# Preflop concluded")
            is_round_concluded = self.dealer.play_flop()
            if not is_round_concluded:
                print("# Flop concluded")
                is_round_concluded = self.dealer.play_turn()
                if not is_round_concluded:
                    print("# Turn concluded")
                    self.dealer.play_river()
        print("# Round ended")
        # todo test button marker is moved

