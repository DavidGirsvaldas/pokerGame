from engine.card import Card
from typing import List


class Player:

    def __init__(self):
        self.hand = []

    def receive_cards(self, cards: List[Card]):
        self.hand = cards
