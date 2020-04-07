from pypokerengine.utils.card_utils import estimate_hole_card_win_rate, gen_cards

from engine.player import Player
from engine.suit import Suit


class ComputerPlayer(Player):

    def receive_cards(self, cards):
        super().receive_cards(cards)
        self.estimate_chance_of_winning()

    def see_community_cards(self, cards):
        super().see_community_cards(cards)
        self.estimate_chance_of_winning()

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
        return gen_cards([suit_representation + rank_representation])[0]

    def estimate_chance_of_winning(self):
        card_representations = [self.convert_card_representation(card) for card in self.cards]
        community_card_representations = [self.convert_card_representation(card) for card in self.community_cards]
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=1000,
            nb_player=5,
            hole_card=card_representations,
            community_card=community_card_representations
        )
        print(win_rate)
        return win_rate
