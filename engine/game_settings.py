from engine.console_player import ConsolePlayer
from engine.player import Player


class DefaultGameSettings:

    def __init__(self):
        self.initial_stack = 5000
        self.small_blind_size = 25
        console_player = ConsolePlayer("ConsolePlayer", self.initial_stack)
        player0 = Player("Player0", self.initial_stack)
        player1 = Player("Player1", self.initial_stack)
        player2 = Player("Player2", self.initial_stack)
        player3 = Player("Player3", self.initial_stack)
        self.players = [console_player, player0, player1, player2, player3]
