import random

from CardLib import Hand

class Player:
    def __init__(self, label, is_ai=False):
        self.is_ai = is_ai
        self.hand = Hand([])
        self.label = label
        self.win_count = 0

    def __str__(self):
        return self.label + ': ' + str(self.hand)
        
    def get_label(self):
        return self.label

    def get_win_count(self):
        return self.win_count

    def round_winner(self):
        self.win_count = self.win_count + 1

    def get_amount_of_cards(self):
        return len(self.hand)

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def add_cards_to_hand(self, cards):
        for card in cards:
            self.add_card(card)

    def play_card(self, number =-1):
        if self.is_ai:
            number = random.randint(0, len(self.hand) - 1)
        tempcard = self.hand.get_card_at(number)
        self.hand.rem_card(tempcard)
        return tempcard

    def clear_hand(self):
        self.hand.rem_all_cards()