from engine.action import Action
from engine.player import Player


class ConsolePlayer(Player):

    def act(self, required_amount_in_pot):
        user_entered_amount = int(input())
        if user_entered_amount == 0:
            return Action.ACTION_FOLD, 0
        if user_entered_amount > required_amount_in_pot:
            return Action.ACTION_RAISE, user_entered_amount
        return Action.ACTION_CALL, required_amount_in_pot

    def receive_cards(self, cards):
        print("Cards received: "+", ".join([str(card) for card in cards]))
        super(ConsolePlayer, self).receive_cards(cards)