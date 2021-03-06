from dataclasses import dataclass


@dataclass(order=True, eq=True)
class Combination:
    strength: int
    kickers: []

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
