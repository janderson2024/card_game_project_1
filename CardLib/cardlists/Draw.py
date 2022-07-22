from CardLib import Card_List


class Draw(Card_List):
    
    def pop_card(self):
        c = self.card_list.pop()
        c.displayable = True
        return c
