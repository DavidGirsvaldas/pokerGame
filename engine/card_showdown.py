from engine import combination_finder
from engine.card import Card
from engine.combination import Combination
from engine.player import Player


def find_winners(players: [Player], common_cards: [Card]):
    if len(common_cards) < 5:
        raise ValueError("Expected 5 community cards, found " + str(len(common_cards)))
    combo_by_player = dict()
    for player in players:
        player_combo = combination_finder.find(player.cards + common_cards)
        combo_by_player[player] = player_combo
        print("Player " + str(player) + " has " + str(player_combo))
    highest_combo = max(combo_by_player.values())
    return find_players_sharing_highest_combo(combo_by_player, highest_combo)


def find_players_sharing_highest_combo(combo_by_player: dict, highest_combo: Combination):
    return [player for player, combo in combo_by_player.items() if combo == highest_combo]
