from Card import Card
from Card_List import Card_List


class Hand(Card_List):
    def sort_suit(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.suit, card.value))

    def sort_rank(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.value, card.suit))
