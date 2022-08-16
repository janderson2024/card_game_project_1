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
        self.gui_obj = CardLib.gui.GuiObject(x, y, 5, 90, self.gui_draw)

    def __len__(self) -> int:
        return len(self.card_list)

    def __str__(self) -> str:
        return " ".join([str(card) for card in self.card_list])

    def __iter__(self):
        yield from self.card_list

    def add_card(self, card: Card):
        self.add_card_gui(card)
        self.card_list.append(card)

    def add_card_gui(self, card: Card):
        card.gui_obj.move(self.gui_obj.x + self.gui_obj.width, self.gui_obj.y+5)
        self.gui_obj.width += card.gui_obj.width + 5

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


    def gui_draw(self):
        background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, self.gui_obj.width, self.gui_obj.height+10)
        CardLib.gui.draw_rect((100,100,100), background_rect)

        for card in self.card_list:
            card.gui_obj.draw()