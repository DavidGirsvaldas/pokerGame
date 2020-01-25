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


def find_full_house(cards: List[Card]):
    ranks = [card.rank for card in cards]
    hand = []
    ranks_by_strength = sorted(ranks, reverse=True)
    for i in range(0, len(ranks_by_strength) - 2):
        if ranks_by_strength[i] == ranks_by_strength[i + 1] == ranks_by_strength[i + 2]:
            for _ in range(0, 3):
                hand.append(ranks_by_strength[i])
            break
    if len(hand) == 0:
        return None
    for i in range(0, len(ranks_by_strength) - 1):
        if ranks_by_strength[i] == ranks_by_strength[i + 1] != hand[0]:
            for _ in range(0, 2):
                hand.append(ranks_by_strength[i])
            break
    if len(hand) == 5:
        return Combination(7, hand)
    return None


def find_flush(cards: List[Card]):
    suit_occurrences = defaultdict()
    for card in cards:
        if card.suit not in suit_occurrences:
            suit_occurrences[card.suit] = []
        suit_occurrences[card.suit].append(card.rank)
    for suit in suit_occurrences:
        grouped_by_suit = suit_occurrences[suit]
        if len(grouped_by_suit) > 4:
            sorted_ranks = sorted(grouped_by_suit, reverse=True)
            top_5 = sorted_ranks[:5]
            return Combination(6, top_5)
    return None