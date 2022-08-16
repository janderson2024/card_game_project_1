import CardLib

class Discard(CardLib.CardList):
    def get_top_card(self) -> CardLib.Card:
        if self.card_list:
            return self.card_list[-1]

    def add_card_gui(self, card: CardLib.Card):
        card.gui_obj.move(self.gui_obj.x,self.gui_obj.y)

    def gui_draw(self):
        if len(self) > 0:
            temp_card = self.card_list[-1]
            temp_card.gui_obj.draw()
        else:
            background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, 70, self.gui_obj.height)
            CardLib.gui.draw_rect((100,100,100), background_rect)
