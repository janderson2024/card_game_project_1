from CardLib import CardList, Card
import CardLib


class Hand(CardList):

    def sort_by_suit(self):
        self.card_list = sorted(self.card_list, key=lambda card: (card.suit, 0 - card.value))

    def sort_by_rank(self):
        self.card_list = sorted(self.card_list, key=lambda card: (0 - card.value, card.suit))

    def get_all_valid_cards(self, game_valid_cards: [Card]) -> CardList:
        return CardList(list(filter(game_valid_cards, self.card_list)))

    def gui_draw(self):
        if len(self) > 0:
            temp_card = self.card_list[-1]
            temp_card.gui_obj.draw()
        else:
            background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, 70, self.gui_obj.height)
            CardLib.gui.draw_rect((100, 100, 100), background_rect)

    def __str__(self) -> str:
        return ", ".join([f"{str(num)}) {str(card)}" for num, card in enumerate(self.card_list, start=1)])
