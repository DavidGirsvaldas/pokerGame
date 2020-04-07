from enum import Enum


class Suit(Enum):
    spades = 1
    clubs = 2
    diamonds = 3
    hearts = 4

    def __str__(self):
        suit_names = {
            1: "spades",
            2: "clubs",
            3: "diamonds",
            4: "hearts"
        }
        return suit_names[self.value]
