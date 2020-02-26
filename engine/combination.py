from engine.rank import Rank


class Combination:

    def __init__(self, strength: int, kickers: [Rank] = None):
        self.strength = strength
        self.kickers = kickers

    def __eq__(self, other):
        return self.strength == other.strength and self.kickers == other.kickers

    def __ne__(self, other):
        return self.strength != other.strength or self.kickers != other.kickers

    def __lt__(self, other):
        if self.strength == other.strength:
            for i in range(0, 5):
                if other.kickers[i] == self.kickers[i]:
                    continue
                else:
                    return other.kickers[i] > self.kickers[i]
        return self.strength < other.strength

    def __str__(self):
        switcher = {
            1: "High card",
            2: "Pair",
            3: "Two pairs",
            4: "Three of a kind",
            5: "Straight",
            6: "Flush",
            7: "Full house",
            8: "Four of a kind",
            9: "Straight flush",
            10: "Royal flush"
        }
        readable_kickers_list = "[" + ",".join(str(kicker) for kicker in self.kickers) + "]"
        return switcher[self.strength] + " " + readable_kickers_list
