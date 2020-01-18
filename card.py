import suit
from rank import Rank


class Card():
    rank: Rank
    suit: suit

    def __init__(self, rank: Rank, suit: suit):
        self.rank = rank
        self.suit = suit

