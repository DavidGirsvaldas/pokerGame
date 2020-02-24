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
    highest_combo = find_highest_combo_among_players(combo_by_player)
    return find_players_sharing_highest_combo(combo_by_player, highest_combo)


def find_highest_combo_among_players(combo_by_player: defaultdict):
    highest_combo = Combination(0, [])
    for combo in combo_by_player.values():
        if combo.strength == highest_combo.strength: # todo make into Combination.__comparison__ or whatever its called
            for i in range(0, 5):
                if combo.kickers[i] != highest_combo.kickers[i]:
                    if combo.kickers[i] > highest_combo.kickers[i]:
                        highest_combo = combo
                    break
        else:
            if combo.strength > highest_combo.strength:
                highest_combo = combo
    return highest_combo


def find_players_sharing_highest_combo(combo_by_player: defaultdict, highest_combo: Combination):
    winners = []
    for player, combo in combo_by_player.items():
        if combo == highest_combo:
            print("Winner " + str(player) + " with " + str(combo))
            winners.append(player)
    return winners
