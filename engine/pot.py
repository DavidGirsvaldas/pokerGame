class Pot:

    def __init__(self):
        self.size = 0
        self.players = {}
        self.pots = []

    def total_count(self):
        amount = self.size
        for _, players_chips_in_pot in self.pots[0].players.items():
            amount += players_chips_in_pot
        return amount

    def pot_size(self):
        amount = self.size
        for _, players_chips_in_pot in self.players.items():
            amount += players_chips_in_pot
        return amount

    def player_calls(self, player, amount):
        if len(self.pots) is 0:
            pot = Pot()
            self.pots.append(pot)
            self.players = pot.players
        amount_to_add = amount - player.money_in_pot
        player.stack -= amount_to_add
        if player not in self.pots[0].players:
            self.pots[0].players[player] = 0
        self.pots[0].players[player] += amount_to_add
        player.money_in_pot += amount_to_add
        required_amount_in_pot = max(p.money_in_pot for p in self.pots[0].players)
        if player.money_in_pot < required_amount_in_pot:
            side_pot = Pot()
            self.pots.append(side_pot)
            for p in self.pots[0].players:
                split_amount = p.money_in_pot - player.money_in_pot
                if split_amount > 0:
                    side_pot.players[p] = split_amount
                    self.pots[0].players[p] -= split_amount

    def is_pot_closed(self):
        for player in self.pots[0].players.keys():
            if player.stack is 0:
                return True
        return False
