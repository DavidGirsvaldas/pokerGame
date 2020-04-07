from engine.dealer import Dealer
from engine.game_settings import DefaultGameSettings
from engine.round import Round

game_settings = DefaultGameSettings()
dealer = Dealer(None, game_settings.seating)
round = Round(dealer)
while not round.is_winner_determined():
    round.play_round(game_settings.small_blind_size)
