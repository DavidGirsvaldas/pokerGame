from typing import List

from engine.rank import Rank


class Combination:
    strength: int
    kickers: List[Rank]

    def __init__(self, strength: int):
        self.strength = strength

    def __init__(self, strength: int, kickers: List[Rank]):
        self.strength = strength
        self.kickers = kickers

    def __eq__(self, other):
        return self.strength == other.strength and self.kickers == other.kickers
