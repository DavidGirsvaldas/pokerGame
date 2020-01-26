from typing import Iterable, List

from card import Card
from combination import Combination
from collections import defaultdict


def find_high_card(cards: Iterable[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    return Combination(1, ranks_sorted[:5])


def find_pair(cards: List[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    for i in range(0, len(ranks_sorted) - 1):
        if ranks_sorted[i] == ranks_sorted[i + 1]:
            hand = [ranks_sorted[i], ranks_sorted[i]]
            for rank in ranks_sorted:
                if rank not in hand:
                    hand.append(rank)
                    if len(hand) == 5:
                        return Combination(2, hand)
    return None


def find_two_pairs(cards: List[Card]):
    ranks = [card.rank for card in cards]
    rank_occurrences = defaultdict()
    hand = []
    for rank in ranks:
        if rank not in rank_occurrences:
            rank_occurrences[rank] = 0
        rank_occurrences[rank] += 1
        if rank_occurrences[rank] == 2:
            hand.append(rank)
            hand.append(rank)
    if len(hand) < 4:
        return None
    sorted_hand = sorted(hand, reverse=True)
    top_hand = sorted_hand[:4]
    for rank in sorted(ranks, reverse=True):
        if rank not in top_hand:
            top_hand.append(rank)
            return Combination(3, top_hand)
    return None


def find_three_of_a_kind(cards: List[Card]):
    ranks = [card.rank for card in cards]
    rank_occurrences = defaultdict()
    for rank in ranks:
        if rank not in rank_occurrences:
            rank_occurrences[rank] = 0
        rank_occurrences[rank] += 1
        if rank_occurrences[rank] == 3:
            ranks_sorted = sorted(ranks, reverse=True)
            hand = [rank, rank, rank]
            for sorted_rank in ranks_sorted:
                if sorted_rank != rank:
                    hand.append(sorted_rank)
                    if len(hand) == 5:
                        return Combination(4, hand)
    return None


def find_straight(cards: List[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    for i in range(0, len(ranks_sorted) - 4):
        if ranks_sorted[i] == (ranks_sorted[i + 1] + 1) == (ranks_sorted[i + 2] + 2) == (ranks_sorted[i + 3] + 3) == (
                ranks_sorted[i + 4] + 4):
            return Combination(5, ranks_sorted[i:i + 5])
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


def find_four_of_a_kind(cards: Iterable[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    hand = []
    for i in range(0, len(ranks) - 3):
        if ranks_sorted[i] == ranks_sorted[i + 1] == ranks_sorted[i + 2] == ranks_sorted[i + 3]:
            for _ in range(0, 4):
                hand.append(ranks_sorted[i])
            break
    if len(hand) != 4:
        return None
    for rank in ranks_sorted:
        if rank != hand[0]:
            hand.append(rank)
            return Combination(8, hand)
    return None


def find_straight_flush(cards: List[Card]):
    sort_by_suit = defaultdict()
    for card in cards:
        if card.suit not in sort_by_suit:
            sort_by_suit[card.suit] = []
        sort_by_suit[card.suit].append(card.rank)
    for suit in sort_by_suit:
        suited_ranks = sort_by_suit[suit]
        if len(suited_ranks) > 4:
            sorted_ranks = sorted(suited_ranks, reverse=True)
            for i in range(0, len(suited_ranks) - 4):
                if sorted_ranks[i] == (sorted_ranks[i + 1] + 1) == (sorted_ranks[i + 2] + 2) == (
                        sorted_ranks[i + 3] + 3) == (sorted_ranks[i + 4] + 4):
                    return Combination(9, sorted_ranks[i:i + 5])
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
