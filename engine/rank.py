from enum import IntEnum


class Rank(IntEnum):
    r2 = 2
    r3 = 3
    r4 = 4
    r5 = 5
    r6 = 6
    r7 = 7
    r8 = 8
    r9 = 9
    r10 = 10
    Jack = 11
    Queen = 12
    King = 13
    Ace = 14

    def __str__(self):
        switcher = {
            11: "Jack",
            12: "Queen",
            13: "King",
            14: "Ace"
        }
        if self.value in switcher:
            return switcher[self.value]
        return str(self.value)
