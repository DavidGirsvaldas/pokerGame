from dataclasses import dataclass
from engine.dealer import Dealer


@dataclass
class Round:
    dealer: Dealer

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
        self.dealer.move_button()
