from engine.rank import Rank
from engine.suit import Suit
from engine.card import Card
import random


class Deck:
    def __init__(self):
        self.cards = None

    def initialize(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)
