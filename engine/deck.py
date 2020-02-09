from engine.rank import Rank
from engine.suit import Suit
from engine.card import Card


class Deck:
    def __init__(self):
        self.cards = None

    def initialize(self):
        self.cards = set()
        for suit in Suit:
            for rank in Rank:
                self.cards.add(Card(rank, suit))