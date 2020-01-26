from card import Card
from typing import List


class Player:
    hand: List[Card]

    def __init__(self, cards: List[Card]):
        self.hand = cards
