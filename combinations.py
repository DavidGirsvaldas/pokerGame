from typing import Iterable, List

from card import Card
from combination import Combination
from rank import Rank
from collections import defaultdict


def find_high_card(ranks: Iterable[Rank]):
    max_rank = 0
    for rank in ranks:
        if rank.value > max_rank:
            max_rank = rank
    return Rank(max_rank)


def find_four_of_a_kind(ranks: Iterable[Rank]):
    rank_occupancies = defaultdict()
    for rank in ranks:
        if not (rank in rank_occupancies):
            rank_occupancies[rank] = 0
        rank_occupancies[rank] += 1
        if rank_occupancies[rank] == 4:
            return rank
    return None


def is_royal_flush(cards: Iterable[Card]):
    high_cards = defaultdict()
    for card in cards:
        if card.rank.value > 9:
            if card.suit not in high_cards:
                high_cards[card.suit] = defaultdict()
            high_cards[card.suit][card.rank.value] = card.rank.value
    for suit in high_cards:
        contains_royal_flush = True
        for i in range(10, 15):
            if i not in high_cards[suit]:
                contains_royal_flush = False
                break
        if contains_royal_flush:
            return True
    return False


def find_full_house(test_input: List[Card]):
    rank_occurrences = defaultdict()
    for card in test_input:
        if card.rank not in rank_occurrences:
            rank_occurrences[card.rank] = 0
        rank_occurrences[card.rank] += 1
    three_of_a_king = None
    pair = None
    for rank, occurrence in rank_occurrences.items():
        if occurrence == 3:
            three_of_a_king = rank
        if occurrence == 2:
            pair = rank
    if three_of_a_king is not None and pair is not None:
        return Combination(7, [three_of_a_king, pair])
    return None
