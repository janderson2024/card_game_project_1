import random

from Card import Card


class Card_List:
    card_list = []

    def __init__(self, cards):
        self.card_list = cards

    def __len__(self):
        return len(self.card_list)

    def __str__(self):
        return " ".join([str(card) for card in self.card_list])

    def add_card(self, card):
        self.card_list.append(card)

    def add_cards(self, cards):
        for card in cards.card_list:
            self.card_list.append(card)

    def rem_card(self, card):
        self.card_list.remove(card)

    def rem_cards(self, cards):
        for card in cards.card_list:
            self.card_list.remove(card)

    def num_cards_left(self):
        return len(self)

    def shuffle(self):
        random.shuffle(self.card_list)

    def get_card_list(self):
        return self

    def set_52_lo(self):
        self.card_list = []
        for suit in range(4):
            for rank in range(13):
                self.add_card(Card(suit, rank))

    def set_54_lo(self):
        self.set_52_lo()
        self.add_card(Card(4, 14))
        self.add_card(Card(4, 15))

    def set_52_hi(self):
        self.card_list = []
        for suit in range(4):
            for rank in range(1, 14):
                self.add_card(Card(suit, rank))

    def set_54_hi(self):
        self.set_52_hi()
        self.add_card(Card(4, 14))
        self.add_card(Card(4, 15))

