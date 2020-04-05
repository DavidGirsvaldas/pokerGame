from engine.action import Action
from engine.dealer import Dealer
from engine.game_settings import DefaultGameSettings
from engine.round import Round
from engine.seating import Seating


def action_check_call():
    def player_action_call(amount):
        return Action.ACTION_CALL, amount

    return player_action_call


game_settings = DefaultGameSettings()
seating = Seating(game_settings.players)
dealer = Dealer(None, seating)
round = Round(dealer)
round.play_round(game_settings.small_blind_size)
