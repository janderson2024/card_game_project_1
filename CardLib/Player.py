import random

import CardLib


class Player:
    PATH_TO_IMG_DIR = "CardLib/card_images/standard/"

    def __init__(self, label: str, is_ai: bool = False, x=0, y=0):
        self.is_ai = is_ai
        self.hand = CardLib.Hand([])
        self.label = label
        self.win_count = 0
        self._init_gui(x, y)

    def _init_gui(self, x, y):
        self.gui_label = CardLib.gui.GuiLabel(self.label, x=x, y=y)
        hand_y = self.gui_label.gui_obj.height + y
        self.hand.gui_obj.move(x, hand_y)

        width = max(self.hand.gui_obj.width, self.gui_label.gui_obj.width)
        height = self.gui_label.gui_obj.height + self.hand.gui_obj.height + 10
        self.gui_obj = CardLib.gui.GuiObject(x, y, width, height, self.gui_draw)

        self.example_card = CardLib.Card(1,1, x=x, y=hand_y)
        self.example_card.set_display()

    def __str__(self) -> str:
        return self.label + ': ' + str(self.hand)

    def __repr__(self)-> str:
        return str(self)

    def get_label(self) -> str:
        return self.label

    def get_win_count(self) -> int:
        return self.win_count

    def round_winner(self):
        self.win_count = self.win_count + 1

    def get_amount_of_cards(self) -> int:
        return len(self.hand)

    def add_card_to_hand(self, card: CardLib.Card):
        self.hand.add_card(card)
        self.resize_gui()

    def add_cards_to_hand(self, cards: [CardLib.Card]):
        for card in cards:
            self.hand.add_card(card)

    def play_card(self, number: int = -1) -> CardLib.Card:
        if self.is_ai and number == -1:
            number = random.randint(0, len(self.hand) - 1)
        temp_card = self.hand.get_card_at(number)
        self.hand.rem_card(temp_card)
        self.resize_gui()
        return temp_card

    def clear_hand(self):
        self.hand.rem_all_cards()
        self.resize_gui()

    def resize_gui(self):
        width = max(self.hand.gui_obj.width, self.gui_label.gui_obj.width)
        height = self.gui_label.gui_obj.height + self.hand.gui_obj.height + 10

        if self.is_ai:
            width = self.gui_label.gui_obj.width
            height -= 10

        self.gui_obj.resize(width,height)

    def gui_draw(self):
        self.gui_label.gui_obj.draw()

        # if self.is_ai:
        #     self.example_card.gui_obj.draw()
        #     card_count_x = self.example_card.gui_obj.width + self.example_card.gui_obj.x + 5
        #     card_count_y = self.example_card.gui_obj.y + (CardLib.CARD_WIDTH // 2)
        #     self.card_count = CardLib.gui.GuiLabel("x " + str(len(self.hand)), x=card_count_x, y=card_count_y)
        #
        #     self.card_count.gui_obj.draw()
        if self.is_ai:
            if len(self.hand) >= 8:
                hand_img = self.PATH_TO_IMG_DIR + "8_card_back.png"
                hand_width = self.example_card.gui_obj.width + 32
                hand_height = self.example_card.gui_obj.height + 24
            else:
                hand_img = self.PATH_TO_IMG_DIR + f"{str(len(self.hand))}_card_back.png"
                hand_width = self.example_card.gui_obj.width+(4*len(self.hand))
                hand_height = self.example_card.gui_obj.height+(3*len(self.hand))
            self.hand_img = CardLib.gui.create_img(hand_img, hand_width, hand_height)
            CardLib.gui.draw_img(self.hand_img, self.gui_obj.x, self.gui_obj.y + 40)

            card_count_x = hand_width + self.gui_obj.x + 5
            card_count_y = self.example_card.gui_obj.y + (CardLib.CARD_WIDTH // 2)
            self.card_count = CardLib.gui.GuiLabel("x " + str(len(self.hand)), x=card_count_x, y=card_count_y)

            self.card_count.gui_obj.draw()
        else:
            self.hand.gui_obj.draw()
