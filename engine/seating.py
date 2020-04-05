from dataclasses import dataclass

from engine.player import Player


@dataclass
class Seating:
    players: [Player]
    button_position = 0

    def button_player(self):
        return self.players[self.button_position]

    def small_blind_player(self):
        return self.next_player_after_position(self.button_position)

    def big_blind_player(self):
        if self.button_position == len(self.players) - 2:
            return self.players[0]
        if self.button_position == len(self.players) - 1:
            return self.players[1]
        return self.players[self.button_position + 2]

    def next_player_after_position(self, position):
        if position == len(self.players) - 1:
            return self.players[0]
        return self.players[position + 1]

    def next_player_after_player(self, player):
        position = self.players.index(player)
        return self.next_player_after_position(position)

    def move_button(self):
        if self.button_position == len(self.players) - 1:
            self.button_position = 0
            return
        self.button_position += 1
