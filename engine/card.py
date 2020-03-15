from .suit import Suit
from .rank import Rank


class Card:

    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        return hash((self.rank, self.suit))

    def __str__(self):
        return str(self.rank) + " of " + str(self.suit)