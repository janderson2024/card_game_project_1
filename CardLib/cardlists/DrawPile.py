from CardLib import CardList, Card


class DrawPile(CardList):

    def pop_card(self, display: bool = True) -> Card:
        card = self.card_list.pop()
        card.displayable = display
        return card
