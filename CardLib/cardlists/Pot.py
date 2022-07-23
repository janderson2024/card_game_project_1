from CardLib import CardList


class Pot(CardList):

    def get_highest_card(self):
        return max(self.card_list)

    def get_winning_card(self):
        # TODO Should be changed depending on game.
        return self.get_highest_card()
