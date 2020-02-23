from enum import Enum


class Suit(Enum):
    spades = 1
    clubs = 2
    diamonds = 3
    hearths = 4

    def __str__(self):
        switcher = {
            1: "spades",
            2: "clubs",
            3: "diamonds",
            4: "hearts"
        }
        return switcher[self.value]
