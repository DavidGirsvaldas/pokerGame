from typing import List
from card import Card
import combinations


def find(cards: List[Card]):
    combo = combinations.find_royal_flush(cards)
    if combo is not None:
        return combo
    combo = combinations.find_straight_flush(cards)
    if combo is not None:
        return combo
    combo = combinations.find_four_of_a_kind(cards)
    if combo is not None:
        return combo
    combo = combinations.find_full_house(cards)
    if combo is not None:
        return combo
    combo = combinations.find_flush(cards)
    if combo is not None:
        return combo
    combo = combinations.find_straight(cards)
    if combo is not None:
        return combo
    combo = combinations.find_three_of_a_kind(cards)
    if combo is not None:
        return combo
    combo = combinations.find_two_pairs(cards)
    if combo is not None:
        return combo
    combo = combinations.find_pair(cards)
    if combo is not None:
        return combo
    return combinations.find_high_card(cards)
