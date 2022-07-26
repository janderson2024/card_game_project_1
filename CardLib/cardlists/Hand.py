from CardLib import CardList


class Hand(CardList):

    def sort_suit(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.suit, 0 - card.value))

    def sort_rank(self):
        self.card_list = sorted(self.card_list, key=lambda card: (0 - card.value, card.suit))

    def get_all_valid_cards(self, game_valid_cards):
        return CardList(list(filter(game_valid_cards, self.card_list)))

    def __str__(self):
        return ", ".join([f"{str(num)}) {str(card)}" for num, card in enumerate(self.card_list, start=1)])