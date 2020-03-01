from engine import card_showdown
from engine.action import Action
from engine.deck import Deck
from engine.pot import Pot


class Dealer:

    def __init__(self, deck, seating, random_seed_for_shuffling=None):
        self.community_cards = []
        self.deck = deck
        self.seating = seating
        self.pot = None
        self.big_blind_size = None
        self.random_seed_for_shuffling = random_seed_for_shuffling

    def deal_cards_to_players(self):
        for player in self.seating.players:
            player.receive_cards(self.deck.draw(2))

    def move_button(self):
        if self.seating.button_pos == len(self.seating.players) - 1:
            self.seating.button_pos = 0
            return
        self.seating.button_pos += 1

    def collect_blinds(self, small_blind_size):
        sb_player = self.seating.small_blind_player()
        bb_player = self.seating.big_blind_player()
        available_size_of_small_blind = min(small_blind_size, sb_player.stack)
        self.take_chips(sb_player, available_size_of_small_blind)
        available_size_of_big_blind = min(small_blind_size * 2, bb_player.stack)
        self.take_chips(bb_player, available_size_of_big_blind)

    def setup_deck(self):
        self.deck = Deck()
        self.deck.initialize()
        self.deck.shuffle(self.random_seed_for_shuffling)

    def add_community_cards(self, card_count):
        self.community_cards += self.deck.draw(card_count)
        print("Community cards: " + ", ".join([str(card) for card in self.community_cards]))

    def take_chips(self, player, amount):
        player.stack -= amount
        player.money_in_pot += amount
        self.pot.size += amount
        if player not in self.pot.players:
            self.pot.players.append(player)

    def play_preflop(self, small_blind_size):
        self.big_blind_size = small_blind_size * 2
        self.pot = Pot()
        self.collect_blinds(small_blind_size)
        self.deal_cards_to_players()
        bb_player = self.seating.big_blind_player()
        amount_to_match = small_blind_size * 2
        return self.ask_players_for_actions(bb_player, amount_to_match, True)

    def play_flop(self):
        self.add_community_cards(3)
        last_player_to_go = self.seating.players[0]  # todo remove assumption that button sits at position 0
        return self.ask_players_for_actions(last_player_to_go, last_player_to_go.money_in_pot, True)

    def play_turn(self):
        self.add_community_cards(1)
        last_player_to_go = self.seating.players[0]  # todo remove assumption that button sits at position 0
        return self.ask_players_for_actions(last_player_to_go, last_player_to_go.money_in_pot, True)

    def play_river(self):
        self.add_community_cards(1)
        last_player_to_go = self.seating.players[0]  # todo remove assumption that button sits at position 0
        winner = self.ask_players_for_actions(last_player_to_go, last_player_to_go.money_in_pot, True)
        if winner:
            return winner
        else:
            # todo bug. can be more than one winner
            winner = card_showdown.find_winner(self.pot.players, self.community_cards)[0]
            return self.award_player_as_winner(winner)

    def ask_players_for_actions(self, player_who_raised, new_raised_amount, include_last_player):
        next_player = self.seating.next_player_after_player(player_who_raised)
        amount_of_calls_to_make = len(self.seating.players)
        if not include_last_player:
            amount_of_calls_to_make -= 1
        for i in range(amount_of_calls_to_make):
            if next_player.cards:
                p_action, p_amount = next_player.act(new_raised_amount)
                if p_action == Action.ACTION_FOLD:
                    print(str(next_player) + " folds")
                    self.player_folds(next_player)
                elif p_action == Action.ACTION_CALL:
                    print(str(next_player) + " calls " + str(p_amount))
                    self.player_calls(next_player, p_amount)
                elif p_action == Action.ACTION_RAISE:
                    print(str(next_player) + " raises to " + str(p_amount))
                    self.player_calls(next_player, p_amount)
                    return self.ask_players_for_actions(next_player, p_amount, False)
                if self.is_winner_determined():
                    return self.award_winner()
            next_player = self.seating.next_player_after_player(next_player)

    def player_calls(self, player, amount):
        player.stack -= amount - player.money_in_pot
        if player not in self.pot.players:
            self.pot.players.append(player)
        self.pot.size += amount - player.money_in_pot
        player.money_in_pot += amount - player.money_in_pot

    def is_winner_determined(self):
        return len(self.pot.players) == 1

    def award_winner(self):
        winner = self.pot.players[0]
        winner.stack += self.pot.size
        return winner

    def award_player_as_winner(self, player):
        player.stack += self.pot.size
        return player

    def player_folds(self, player):
        player.money_in_pot = 0
        player.cards = None
        if player in self.pot.players:
            self.pot.players.remove(player)
