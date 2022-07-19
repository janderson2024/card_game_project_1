from Card import Card
from Card_List import Card_List


class Hand(Card_List):
    def sort_suit(self):
        sorted(self.card_list, key=Card.suit)
