from .rank import Rank
from .suit import Suit
from .card import Card
import random


class Deck:
    def __init__(self):
        self.cards = None

    def initialize(self):
        self.cards = []
        for suit in Suit:
            for rank in Rank:
                self.cards.append(Card(rank, suit))

    def shuffle(self, random_seed = None):
        if random_seed:
            random.Random(random_seed).shuffle(self.cards)
        else:
            random.shuffle(self.cards)

    def draw(self, count):
        return [self.cards.pop() for _ in range(count)]
