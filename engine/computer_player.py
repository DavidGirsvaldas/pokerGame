from pypokerengine.engine.card import Card
from pypokerengine.utils.card_utils import estimate_hole_card_win_rate, gen_cards

from engine.action import Action
from engine.player import Player
from engine.suit import Suit


class ComputerPlayer(Player):

    def act(self, amount):
        chance = self.estimate_chance_of_winning(self.cards, self.community_cards)
        if chance < 0.15 and amount > self.money_in_pot:
            return Action.ACTION_FOLD, 0
        if chance > 0.3:
            if amount < self.stack + self.money_in_pot:
                return Action.ACTION_RAISE, amount + 100
            return Action.ACTION_CALL, self.stack + self.money_in_pot
        return Action.ACTION_CALL, amount

    def convert_card_representation(self, local_card_format):
        suit_converter = {
            Suit.hearts: 'H',
            Suit.diamonds: 'D',
            Suit.spades: 'S',
            Suit.clubs: 'C'
        }
        suit_representation = suit_converter[local_card_format.suit]
        rank_converter = {
            10: "T",
            11: "J",
            12: "Q",
            13: "K",
            14: "A"
        }
        if local_card_format.rank in rank_converter:
            rank_representation = rank_converter[local_card_format.rank]
        else:
            rank_representation = str(local_card_format.rank)
        return Card.from_str(suit_representation + rank_representation)

    def estimate_chance_of_winning(self, player_cards, community_cards):
        card_representations = [self.convert_card_representation(card) for card in player_cards]
        community_card_representations = [self.convert_card_representation(card) for card in community_cards]
        win_rate = self.estimate_winrate(card_representations, community_card_representations)
        return win_rate

    def estimate_winrate(self, card_representations, community_card_representations):
        return estimate_hole_card_win_rate(
            nb_simulation=1000,
            nb_player=5,
            hole_card=card_representations,
            community_card=community_card_representations
        )
