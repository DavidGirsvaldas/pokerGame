from dataclasses import dataclass

from engine.suit import Suit
from engine.rank import Rank


@dataclass(eq=True, frozen=True)
class Card:
    rank: Rank
    suit: Suit

    def __str__(self):
        return str(self.rank) + " of " + str(self.suit)
