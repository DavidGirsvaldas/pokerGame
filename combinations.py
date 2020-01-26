from typing import Iterable, List

from card import Card
from combination import Combination
from rank import Rank
from collections import defaultdict


def find_high_card(cards: Iterable[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    return Combination(1, ranks_sorted[:5])


def find_four_of_a_kind(cards: Iterable[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    hand = []
    for i in range(0, len(ranks)-3):
        if ranks_sorted[i] == ranks_sorted[i+1] == ranks_sorted[i+2] == ranks_sorted[i+3]:
            for _ in range(0, 4):
                hand.append(ranks_sorted[i])
            break
    if len(hand)!=4:
        return None
    for rank in ranks_sorted:
        if rank != hand[0]:
            hand.append(rank)
            return Combination(8, hand)
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
            return Combination(10, sorted(high_cards[suit], reverse=True))
    return None


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
