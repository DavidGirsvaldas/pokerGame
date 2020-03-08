from collections import defaultdict


class Pot:

    def __init__(self):
        self.size = 0
        self.players = defaultdict(int)
        self.side_pot = None

    def total_count(self):
        amount = self.size
        for _, players_chips_in_pot in self.players.items():
            amount += players_chips_in_pot
        return amount

    def pot_size(self):
        amount = self.size
        for _, players_chips_in_pot in self.players.items():
            amount += players_chips_in_pot
        return amount

    def player_calls(self, player, amount):
        amount_to_add = amount - self.players[player]
        player.stack -= amount_to_add
        self.players[player] += amount_to_add
        player.money_in_pot += amount_to_add
        required_amount_in_pot = max(self.players.values())
        player_doesnt_have_enough = self.players[player] < required_amount_in_pot
        other_pot_players_cant_match_bet_made = self.pot_max_size() and self.players[player] > self.pot_max_size()
        if player_doesnt_have_enough or other_pot_players_cant_match_bet_made:
            for p in self.players:
                split_amount = self.players[p] - self.players[player]
                if split_amount > 0:
                    if not self.side_pot:
                        self.side_pot = Pot()
                    self.players[p] -= split_amount
                    self.side_pot.player_calls(p, split_amount + self.side_pot.players[p])

    def get_all_pots(self):
        pots = [self]
        side_pot = self.side_pot
        while side_pot:
            pots.append(side_pot)
            side_pot = side_pot.side_pot
        return pots

    def pot_max_size(self):
        for player in self.players.keys():
            if player.stack is 0:
                return self.players[player]
        return None
