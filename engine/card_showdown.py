from collections import defaultdict
from typing import List

from engine.card import Card
from engine.combination import Combination
from engine.player import Player
from engine import combination_finder


def find_winner(players: List[Player], common_cards: List[Card]):
    combo_by_player = defaultdict()
    for player in players:
        combo_by_player[player] = combination_finder.find(player.hand + common_cards)

    highest_combo = Combination(0, [])
    for combo in combo_by_player.values():
        if combo.strength == highest_combo.strength:
            for i in range(0, 5):
                if combo.kickers[i] != highest_combo.kickers[i]:
                    if combo.kickers[i] > highest_combo.kickers[i]:
                        highest_combo = combo
                    break
        else:
            if combo.strength > highest_combo.strength:
                highest_combo = combo
    winners = []
    for player, combo in combo_by_player.items():
        if combo == highest_combo:
            winners.append(player)
    return winners
