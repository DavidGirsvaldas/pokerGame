from engine.computer_player import ComputerPlayer
from engine.console_player import ConsolePlayer
from engine.seating import Seating


class DefaultGameSettings:

    def __init__(self):
        self.initial_stack = 5000
        self.small_blind_size = 25
        player0 = ComputerPlayer("Player0", self.initial_stack)
        player1 = ComputerPlayer("Player1", self.initial_stack)
        player2 = ComputerPlayer("Player2", self.initial_stack)
        player3 = ComputerPlayer("Player3", self.initial_stack)
        players = [player0, player1, player2, player3]
        console_player = ConsolePlayer("ConsolePlayer", self.initial_stack)
        players.append(console_player)
        self.seating = Seating(players)
