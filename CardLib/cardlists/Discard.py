from CardLib import Card_List


class Discard(Card_List):
    def get_top_card(self):
        if not self.card_list:
            return None
        else:
            return self.card_list[-1]
