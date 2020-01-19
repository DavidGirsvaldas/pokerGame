from typing import List

from rank import Rank


class Combination:
    strength: int
    kickers: List[Rank]

    def __init__(self, strength: int):
        self.strength = strength

    def __init__(self, strength: int, kickers: List[Rank]):
        self.strength = strength
        self.kickers = kickers
