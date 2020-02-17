from typing import Iterable, List

from engine.card import Card
from engine.combination import Combination
from collections import defaultdict

from engine.rank import Rank


def find_high_card(cards: Iterable[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    return Combination(1, ranks_sorted[:5])


def find_pair(cards: List[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    for i in range(len(ranks_sorted) - 1):
        if ranks_sorted[i] == ranks_sorted[i + 1]:
            hand = [ranks_sorted[i], ranks_sorted[i]]
            for rank in ranks_sorted:
                if rank not in hand:
                    hand.append(rank)
                    if len(hand) == 5:
                        return Combination(2, hand)


def find_two_pairs(cards: List[Card]):
    ranks = [card.rank for card in cards]
    rank_occurrences = defaultdict(int)
    hand = []
    for rank in ranks:
        rank_occurrences[rank] += 1
        if rank_occurrences[rank] == 2:
            hand += 2 * [rank]
    if len(hand) < 4:
        return
    sorted_hand = sorted(hand, reverse=True)
    top_hand = sorted_hand[:4]
    for rank in sorted(ranks, reverse=True):
        if rank not in top_hand:
            top_hand.append(rank)
            return Combination(3, top_hand)


def find_three_of_a_kind(cards: List[Card]):
    ranks = [card.rank for card in cards]
    rank_occurrences = defaultdict(int)
    for rank in ranks:
        rank_occurrences[rank] += 1
        if rank_occurrences[rank] == 3:
            ranks_sorted = sorted(ranks, reverse=True)
            hand = 3 * [rank]
            for sorted_rank in ranks_sorted:
                if sorted_rank != rank:
                    hand.append(sorted_rank)
                    if len(hand) == 5:
                        return Combination(4, hand)


def find_straight(cards: List[Card]):
    ranks = [card.rank for card in cards]
    unique_ranks = list(dict.fromkeys(ranks))
    ranks_sorted = sorted(unique_ranks, reverse=True)
    straight_starting_ace = [Rank.Ace, Rank.r5, Rank.r4, Rank.r3, Rank.r2]
    if all(x in ranks_sorted for x in straight_starting_ace):
        return Combination(5, [Rank.r5, Rank.r4, Rank.r3, Rank.r2, Rank.Ace])
    for i in range(len(ranks_sorted) - 4):
        if ranks_sorted[i] == (ranks_sorted[i + 1] + 1) == (ranks_sorted[i + 2] + 2) == (ranks_sorted[i + 3] + 3) == (ranks_sorted[i + 4] + 4):
            return Combination(5, ranks_sorted[i:i + 5])


def find_flush(cards: List[Card]):
    suit_occurrences = defaultdict(list)
    for card in cards:
        suit_occurrences[card.suit].append(card.rank)
    for suit in suit_occurrences:
        grouped_by_suit = suit_occurrences[suit]
        if len(grouped_by_suit) > 4:
            sorted_ranks = sorted(grouped_by_suit, reverse=True)
            top_5 = sorted_ranks[:5]
            return Combination(6, top_5)


def find_full_house(cards: List[Card]):
    ranks = [card.rank for card in cards]
    hand = []
    ranks_by_strength = sorted(ranks, reverse=True)
    for i in range(len(ranks_by_strength) - 2):
        if ranks_by_strength[i] == ranks_by_strength[i + 1] == ranks_by_strength[i + 2]:
            hand += 3 * [ranks_by_strength[i]]
            break
    if len(hand) == 0:
        return
    for i in range(len(ranks_by_strength) - 1):
        if ranks_by_strength[i] == ranks_by_strength[i + 1] != hand[0]:
            hand += 2 * [ranks_by_strength[i]]
            break
    if len(hand) == 5:
        return Combination(7, hand)


def find_four_of_a_kind(cards: Iterable[Card]):
    ranks = [card.rank for card in cards]
    ranks_sorted = sorted(ranks, reverse=True)
    hand = []
    for i in range(len(ranks) - 3):
        if ranks_sorted[i] == ranks_sorted[i + 1] == ranks_sorted[i + 2] == ranks_sorted[i + 3]:
            hand += 4 * [ranks_sorted[i]]
            break
    if len(hand) != 4:
        return
    for rank in ranks_sorted:
        if rank != hand[0]:
            hand.append(rank)
            return Combination(8, hand)


def find_straight_flush(cards: List[Card]):
    sort_by_suit = defaultdict(list)
    for card in cards:
        sort_by_suit[card.suit].append(card.rank)
    for suit in sort_by_suit:
        suited_ranks = sort_by_suit[suit]
        if len(suited_ranks) > 4:
            sorted_ranks = sorted(suited_ranks, reverse=True)
            for i in range(len(suited_ranks) - 4):
                if sorted_ranks[i] == (sorted_ranks[i + 1] + 1) == (sorted_ranks[i + 2] + 2) == (
                        sorted_ranks[i + 3] + 3) == (sorted_ranks[i + 4] + 4):
                    return Combination(9, sorted_ranks[i:i + 5])


def find_royal_flush(cards: Iterable[Card]):
    high_cards = defaultdict(dict)
    for card in cards:
        if card.rank.value > 9:
            high_cards[card.suit][card.rank.value] = card.rank.value
    for suit in high_cards:
        contains_royal_flush = True
        for i in range(10, 15):
            if i not in high_cards[suit]:
                contains_royal_flush = False
                break
        if contains_royal_flush:
            return Combination(10, sorted(high_cards[suit], reverse=True))
