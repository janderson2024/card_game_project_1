from CardLib import CardList, Card


class Draw(CardList):

    def pop_card(self, display: bool = True) -> Card:
        card = self.card_list.pop()
        card.displayable = display
        return card
