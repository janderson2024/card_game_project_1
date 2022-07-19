from Card import Card
from card_list.Card_List import Card_List


class Draw(Card_List):
    def set_52_lo(self):
        self.card_list = []
        for suit in range(1, 5):
            for rank in range(1, 14):
                self.add_card(Card(suit, rank, displayable=False))
        self.shuffle()

    def set_54_lo(self):
        self.set_52_lo()
        self.add_card(Card(0, 15, displayable=False))
        self.add_card(Card(0, 16, displayable=False))
        self.shuffle()

    def set_52_hi(self):
        self.card_list = []
        for suit in range(1, 5):
            for rank in range(2, 15):
                self.add_card(Card(suit, rank, displayable=False))
        self.shuffle()

    def set_54_hi(self):
        self.set_52_hi()
        self.add_card(Card(0, 15, displayable=False))
        self.add_card(Card(0, 16, displayable=False))
        self.shuffle()

    def pop_card(self):
        c = self.card_list.pop()
        c.displayable = True
        return c
