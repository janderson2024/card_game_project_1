import CardLib


class Hand(CardLib.CardList):

    def sort_by_suit(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.suit, 0 - card.value))

    def sort_by_rank(self):
        self.card_list = sorted(self.card_list, key=lambda card: (0 - card.value, card.suit))

    def get_all_valid_cards(self, game_valid_cards: callable) -> CardLib.CardList:
        return CardLib.CardList(list(filter(game_valid_cards, self.card_list)))

    #does not implement _init_gui, update_card_pos, or gui_draw as they are the same as CardList

    def __str__(self) -> str:
        return ", ".join([f"{str(num)}) {str(card)}" for num, card in enumerate(self.card_list, start=1)])
