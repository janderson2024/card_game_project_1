from CardLib import CardList


class Draw(CardList):
    
    def pop_card(self):
        c = self.card_list.pop()
        c.displayable = True
        return c
