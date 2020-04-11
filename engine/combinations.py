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
            hand += pick_highest_kickers(hand, ranks_sorted, 3)
            return Combination(2, hand)


def find_two_pairs(cards: List[Card]):
    ranks = [card.rank for card in cards]
    rank_occurrences = count_rank_occurrences(ranks)
    ranks_that_can_form_pair = [rank for rank in rank_occurrences if rank_occurrences[rank] == 2]
    if len(ranks_that_can_form_pair) < 2:
        return
    hand = 2 * [ranks_that_can_form_pair[0]] + 2 * [ranks_that_can_form_pair[1]]
    ranks_sorted = sorted(ranks, reverse=True)
    hand += pick_highest_kickers(hand, ranks_sorted, 1)
    return Combination(3, hand)


def find_three_of_a_kind(cards: List[Card]):
    ranks = [card.rank for card in cards]
    rank_occurrences = count_rank_occurrences(ranks)
    ranks_that_can_form_three_of_a_kind = [rank for rank in rank_occurrences if rank_occurrences[rank] == 3]
    if len(ranks_that_can_form_three_of_a_kind) is 0:
        return
    highest_three_of_a_kind_available = max(ranks_that_can_form_three_of_a_kind)
    hand = 3 * [highest_three_of_a_kind_available]
    ranks_sorted = sorted(ranks, reverse=True)
    hand += pick_highest_kickers(hand, ranks_sorted, 2)
    return Combination(4, hand)


def find_straight(cards: List[Card]):
    ranks = [card.rank for card in cards]
    unique_ranks = list(dict.fromkeys(ranks))
    ranks_sorted = sorted(unique_ranks, reverse=True)
    straight = try_find_straight(ranks_sorted)
    if straight:
        return Combination(5, straight)


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
    three_of_a_kind = find_three_of_a_kind(cards)
    if not three_of_a_kind:
        return
    hand = three_of_a_kind.kickers[:3]
    remaining_cards = [card for card in cards if card.rank not in hand]
    pair = find_pair(remaining_cards)
    if pair:
        hand += pair.kickers[:2]
        return Combination(7, hand)


def find_four_of_a_kind(cards: Iterable[Card]):
    ranks = [card.rank for card in cards]
    rank_occurrences = count_rank_occurrences(ranks)
    for rank, count in rank_occurrences.items():
        if count is 4:
            hand = 4 * [rank]
            ranks_sorted = sorted(ranks, reverse=True)
            hand += pick_highest_kickers(hand, ranks_sorted, 1)
            return Combination(8, hand)


def find_straight_flush(cards: List[Card]):
    sort_by_suit = defaultdict(list)
    for card in cards:
        sort_by_suit[card.suit].append(card.rank)
    for suited_ranks in sort_by_suit.values():
        if len(suited_ranks) > 4:
            sorted_ranks = sorted(suited_ranks, reverse=True)
            straight = try_find_straight(sorted_ranks)
            if straight:
                return Combination(9, straight)


def find_royal_flush(cards: List[Card]):
    straight_flush = find_straight_flush(cards)
    if not straight_flush:
        return
    if straight_flush.kickers[0] is Rank.Ace:
        return Combination(10, straight_flush.kickers)


def try_find_straight(ranks_sorted: [Rank]):
    straight_starting_ace = [Rank.r5, Rank.r4, Rank.r3, Rank.r2, Rank.Ace]
    if all(x in ranks_sorted for x in straight_starting_ace):
        return straight_starting_ace
    for i in range(len(ranks_sorted) - 4):
        if ranks_sorted[i] == (ranks_sorted[i + 1] + 1) == (ranks_sorted[i + 2] + 2) == (ranks_sorted[i + 3] + 3) == (
                ranks_sorted[i + 4] + 4):
            return ranks_sorted[i:i + 5]


def pick_highest_kickers(hand: List[Rank], all_sorted_card_ranks: List[Rank], required_kicker_count: int):
    kickers = [rank for rank in all_sorted_card_ranks if rank not in hand]
    return kickers[:required_kicker_count]


def count_rank_occurrences(ranks: List[Rank]):
    rank_occurrences = defaultdict(int)
    for rank in ranks:
        rank_occurrences[rank] += 1
    return rank_occurrences
