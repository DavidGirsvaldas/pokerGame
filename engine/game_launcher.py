from engine.action import Action
from engine.console_player import ConsolePlayer
from engine.dealer import Dealer
from engine.player import Player
from engine.seating import Seating


def setup_new_player(initial_stack):
    player = Player(initial_stack)
    player.stack = initial_stack
    return player


def action_check_call(player_name):
    def player_action_call(amount):
        print(player_name + " calls " + str(amount))
        return Action.ACTION_CALL, amount

    return player_action_call


initial_stack = 100
small_blind_size = 5
console_player = ConsolePlayer(initial_stack)
button_player = setup_new_player(initial_stack)
sb_player = setup_new_player(initial_stack)
bb_player = setup_new_player(initial_stack)
button_player.act = action_check_call("Player")
sb_player.act = action_check_call("Player")
bb_player.act = action_check_call("Player")

players = [console_player, button_player, sb_player, bb_player]
seating = Seating(players)
dealer = Dealer(None, seating)
dealer.setup_deck()
winner = dealer.play_preflop(small_blind_size)
print("# Preflop concluded")
winner = dealer.play_flop()
print("# Flop concluded")
winner = dealer.play_turn()
print("# Turn concluded")
winner = dealer.play_river()
print("# River concluded")
