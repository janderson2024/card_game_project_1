from CardLib import CardList


class Draw(CardList):

    def pop_card(self, display: bool = True):
        card = self.card_list.pop()
        card.displayable = display
        return card
