from CardLib import Card_List


class Hand(Card_List):

    def sort_suit(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.suit, card.value))

    def sort_rank(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.value, card.suit))

    def get_all_valid_cards(self, game_valid_cards):
        return Card_List(list(filter(game_valid_cards, self.card_list)))

    def __str__(self):
        return ", ".join([f"{str(num)}) {str(card)}" for num, card in enumerate(self.card_list, start=1)])
