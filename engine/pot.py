from collections import defaultdict


class Pot:
    def __init__(self):
        self.size = 0
        self.chips_per_player = defaultdict(int)
        self.side_pot = None

    def total_count(self):
        total_amount = 0
        for pot in self.get_all_pots():
            total_amount += pot.pot_size()
        return total_amount

    def pot_size(self):
        amount = self.size
        amount += sum(self.chips_per_player.values())
        return amount

    def player_calls(self, player, amount):
        def is_pot_split_required():
            player_doesnt_have_enough = self.chips_per_player[player] < max(self.chips_per_player.values())
            other_pot_players_cant_match_bet_made = self.pot_max_size() and self.chips_per_player[player] > self.pot_max_size()
            return player_doesnt_have_enough or other_pot_players_cant_match_bet_made

        amount_to_add = amount - self.chips_per_player[player]
        player.stack -= amount_to_add
        self.chips_per_player[player] += amount_to_add
        player.money_in_pot += amount_to_add
        if is_pot_split_required():
            for p in self.chips_per_player:
                amount_to_leave_in_pot = 99999  # todo -ugly! refactor
                if self.pot_max_size():
                    amount_to_leave_in_pot = self.pot_max_size()
                in_pot = self.chips_per_player[player]
                split_amount = self.chips_per_player[p] - min(in_pot, amount_to_leave_in_pot)
                if split_amount > 0:
                    if not self.side_pot:
                        self.side_pot = Pot()
                    self.chips_per_player[p] -= split_amount
                    p.stack += split_amount
                    self.side_pot.player_calls(p, split_amount + self.side_pot.chips_per_player[p])

    def get_all_pots(self):
        pots = [self]
        side_pot = self.side_pot
        while side_pot:
            pots.append(side_pot)
            side_pot = side_pot.side_pot
        return pots

    def pot_max_size(self):
        all_in_players = [player for player in self.chips_per_player.keys() if player.stack is 0]
        if len(all_in_players) is 0:
            return None
        return min([self.chips_per_player[player] for player in all_in_players])
