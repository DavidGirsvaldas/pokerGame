from engine.action import Action
from engine.console_player import ConsolePlayer
from engine.dealer import Dealer
from engine.player import Player
from engine.round import Round
from engine.seating import Seating

def action_check_call():
    def player_action_call(amount):
        return Action.ACTION_CALL, amount

    return player_action_call


initial_stack = 100
small_blind_size = 5
console_player = ConsolePlayer("ConsolePlayer", initial_stack)
button_player = Player("Player1",initial_stack)
sb_player = Player("Player2",initial_stack)
bb_player = Player("Player3",initial_stack)
button_player.act = action_check_call()
sb_player.act = action_check_call()
bb_player.act = action_check_call()

players = [console_player, button_player, sb_player, bb_player]
seating = Seating(players)
dealer = Dealer(None, seating)
round = Round(dealer)
round.play_round()
