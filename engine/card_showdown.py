from collections import defaultdict

from engine.card import Card
from engine.combination import Combination
from engine.player import Player
from engine import combination_finder


def find_winner(players: [Player], common_cards: [Card]):
    combo_by_player = defaultdict()
    for player in players:
        player_combo = combination_finder.find(player.cards + common_cards)
        combo_by_player[player] = player_combo
        print("Player " + str(player) + " has " + str(player_combo))
    highest_combo = max(combo_by_player.values())
    return find_players_sharing_highest_combo(combo_by_player, highest_combo)


def find_players_sharing_highest_combo(combo_by_player: defaultdict, highest_combo: Combination):
    winners = []
    for player, combo in combo_by_player.items():
        if combo == highest_combo:
            print("Winner " + str(player) + " with " + str(combo))
            winners.append(player)
    return winners
