from collections import defaultdict


class Pot:

    def __init__(self):
        self.size = 0
        self.players = defaultdict(int)
        self.side_pot = None

    def total_count(self):
        total_amount = 0
        for pot in self.get_all_pots():
            total_amount += pot.pot_size()
        return total_amount

    def pot_size(self):
        amount = self.size
        amount += sum(self.players.values())
        return amount

    def player_calls(self, player, amount):
        amount_to_add = amount - self.players[player]
        player.stack -= amount_to_add
        self.players[player] += amount_to_add
        player.money_in_pot += amount_to_add
        player_doesnt_have_enough = self.players[player] < max(self.players.values())
        other_pot_players_cant_match_bet_made = self.pot_max_size() and self.players[player] > self.pot_max_size()
        if player_doesnt_have_enough or other_pot_players_cant_match_bet_made:
            for p in self.players:
                amount_to_leave_in_pot = 99999 # todo -ugly! refactor
                if self.pot_max_size():
                    amount_to_leave_in_pot = self.pot_max_size()
                in_pot = self.players[player]
                split_amount = self.players[p] - min(in_pot, amount_to_leave_in_pot)
                if split_amount > 0:
                    if not self.side_pot:
                        self.side_pot = Pot()
                    self.players[p] -= split_amount
                    p.stack += split_amount
                    self.side_pot.player_calls(p, split_amount + self.side_pot.players[p])

    def get_all_pots(self):
        pots = [self]
        side_pot = self.side_pot
        while side_pot:
            pots.append(side_pot)
            side_pot = side_pot.side_pot
        return pots

    def pot_max_size(self):
        all_in_players = [player for player in self.players.keys() if player.stack is 0]
        if len(all_in_players) is 0:
            return None
        return min([self.players[player] for player in all_in_players])
