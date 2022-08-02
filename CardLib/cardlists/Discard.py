from CardLib import CardList, Card


class Discard(CardList):
    def get_top_card(self) -> Card:
        if self.card_list:
            return self.card_list[-1]
