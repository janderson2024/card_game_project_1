from CardLib import CardList, Card
import CardLib


class Hand(CardList):

    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, 5, 90, self.gui_draw)

    def sort_by_suit(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.suit, 0 - card.value))

    def sort_by_rank(self):
        self.card_list = sorted(self.card_list, key=lambda card: (0 - card.value, card.suit))

    def get_all_valid_cards(self, game_valid_cards: [Card]) -> CardList:
        return CardList(list(filter(game_valid_cards, self.card_list)))

    def __str__(self) -> str:
        return ", ".join([f"{str(num)}) {str(card)}" for num, card in enumerate(self.card_list, start=1)])
