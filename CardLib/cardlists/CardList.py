import random

import CardLib
from CardLib import Card


class CardList:
    def __init__(self, cards=None, x=0, y=0):
        if cards is None:
            cards = []
        self.card_list = cards
        
        self._init_gui(x, y)

    def _init_gui(self, x, y):
        self.x = x
        self.y = y
        self.card_offset = 5
        self.card_height = 70

    def __len__(self) -> int:
        return len(self.card_list)

    def __str__(self) -> str:
        return " ".join([str(card) for card in self.card_list])

    def __iter__(self):
        yield from self.card_list

    def add_card(self, card: Card):
        card.x = self.x + self.card_offset
        card.y = self.y + 5
        self.card_offset += card.width + 5
        self.card_list.append(card)

    def get_card_at(self, index: int) -> Card:
        return self.card_list[index]

    def add_cards(self, cards: [Card]):
        for card in cards:
            self.add_card(card)

    def rem_card(self, card: Card):
        self.card_list.remove(card)

    def rem_cards(self, cards: [Card]):
        for card in cards:
            self.rem_card(card)

    def rem_all_cards(self):
        self.card_list = []

    def num_cards_left(self) -> int:
        return len(self.card_list)

    def shuffle(self):
        random.shuffle(self.card_list)

    def get_card_list(self) -> [Card]:
        return self.card_list

    def contains(self, card) -> bool:
        return card in self.card_list


    def draw(self):
        background_rect = CardLib.gui.create_rect(self.x, self.y, self.card_offset, self.card_height+10)
        CardLib.gui.draw_rect((100,100,100), background_rect)

        for card in self.card_list:
            card.draw()