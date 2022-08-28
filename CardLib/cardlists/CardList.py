import random

import CardLib


class CardList:
    padding = 5
    def __init__(self, cards=None, x=0, y=0):
        if cards is None:
            cards = []
        self.card_list = cards
        
        self._init_gui(x, y)

    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, CardLib.CARD_WIDTH, 90, self.gui_draw)

    def __len__(self) -> int:
        return len(self.card_list)

    def __str__(self) -> str:
        return " ".join([str(card) for card in self.card_list])

    def __iter__(self):
        yield from self.card_list

    def add_card(self, card: CardLib.Card):
        self.card_list.append(card)
        self.update_cards_pos()

    def get_card_at(self, index: int) -> CardLib.Card:
        return self.card_list[index]

    def add_cards(self, cards: [CardLib.Card]):
        for card in cards:
            self.add_card(card)

    def rem_card(self, card: CardLib.Card):
        self.card_list.remove(card)
        self.update_cards_pos()

    def update_cards_pos(self):
        for index, card in enumerate(self.card_list):
            card_x = index * (CardLib.CARD_WIDTH + self.padding) + self.gui_obj.x + self.padding
            card.gui_obj.move(card_x, self.gui_obj.y+self.padding)
        self.gui_obj.width = max((len(self) * (CardLib.CARD_WIDTH + self.padding)) + self.padding, CardLib.CARD_WIDTH)


    def rem_cards(self, cards: [CardLib.Card]):
        for card in cards:
            self.rem_card(card)

    def rem_all_cards(self):
        self.card_list = []

    def num_cards_left(self) -> int:
        return len(self.card_list)

    def shuffle(self):
        random.shuffle(self.card_list)

    def get_card_list(self) -> [CardLib.Card]:
        return self.card_list

    def contains(self, card) -> bool:
        return card in self.card_list


    def gui_draw(self):
        background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, self.gui_obj.width, self.gui_obj.height+10)
        CardLib.gui.draw_rect((100,100,100), background_rect)

        for card in self.card_list:
            card.gui_obj.draw()