import random

from CardLib import Card


class CardList:
	
    def __init__(self, cards):
        self.card_list = cards

    def __len__(self):
        return len(self.card_list)

    def __str__(self):
        return " ".join([str(card) for card in self.card_list])

    def add_card(self, card):
        self.card_list.append(card)

    def get_card_at(self, index):
        return self.card_list[index]

    def add_cards(self, cards):
        for card in cards:
            self.card_list.append(card)

    def rem_card(self, card):
        self.card_list.remove(card)

    def rem_cards(self, cards):
        for card in cards.card_list:
            self.card_list.remove(card)

    def rem_all_cards(self):
        self.card_list = []

    def num_cards_left(self):
        return len(self.card_list)

    def shuffle(self):
        random.shuffle(self.card_list)

    def get_card_list(self):
        return self.card_list

    def is_card_in(self, card):
        return card in self.card_list