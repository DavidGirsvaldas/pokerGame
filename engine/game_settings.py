from engine.action import Action
from engine.console_player import ConsolePlayer
from engine.player import Player


class DefaultGameSettings:

    def __init__(self):
        def action_check_call():
            def player_action_call(amount):
                return Action.ACTION_CALL, amount

            return player_action_call

        self.initial_stack = 5000
        self.small_blind_size = 25
        player0 = Player("Player0", self.initial_stack)
        player1 = Player("Player1", self.initial_stack)
        player2 = Player("Player2", self.initial_stack)
        player3 = Player("Player3", self.initial_stack)
        self.players = [player0, player1, player2, player3]
        for player in self.players:
            player.act = action_check_call()
        console_player = ConsolePlayer("ConsolePlayer", self.initial_stack)
        self.players.append(console_player)
