from typing import Iterable

from card import Card
from rank import Rank
from collections import defaultdict


def find_high_card(ranks: Iterable[Rank]):
    max_rank = 0
    for r in ranks:
        if r.value > max_rank:
            max_rank = r
    return Rank(max_rank)


def find_four_of_a_kind(ranks: Iterable[Rank]):
    rank_occupancies = defaultdict()
    for r in ranks:
        if not (r in rank_occupancies):
            rank_occupancies[r] = 0
        rank_occupancies[r] += 1
        if rank_occupancies[r] == 4:
            return r
    return None


def is_royal_flush(cards: Iterable[Card]):
    high_cards = defaultdict()
    for c in cards:
        if c.rank.value > 9:
            if c.suit not in high_cards:
                high_cards[c.suit] = defaultdict()
            high_cards[c.suit][c.rank.value] = c.rank.value
    for s in high_cards:
        contains_royal_flush = True
        for i in range(10, 15):
            if i not in high_cards[s]:
                contains_royal_flush = False
                break
        if contains_royal_flush:
            return True
    return False
