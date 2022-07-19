from Card_List import Card_List


class Pot(Card_List):
    def get_highest_card(self):
        return max(self.card_list)

    def get_winning_card(self):
        # TODO Should be changed depending on game.
        return self.get_highest_card()
