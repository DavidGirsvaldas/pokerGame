from typing import List
from .card import Card
from . import combinations


def find(cards: List[Card]):
    return combinations.find_royal_flush(cards) or combinations.find_straight_flush(
        cards) or combinations.find_four_of_a_kind(cards) or combinations.find_full_house(
        cards) or combinations.find_flush(cards) or combinations.find_straight(
        cards) or combinations.find_three_of_a_kind(cards) or combinations.find_two_pairs(
        cards) or combinations.find_pair(cards) or combinations.find_high_card(cards)
