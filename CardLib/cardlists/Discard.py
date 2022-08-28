import CardLib


class Discard(CardLib.CardList):
    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, 70, 90, self.gui_draw)
        self.background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, self.gui_obj.width, self.gui_obj.height)

    def get_top_card(self) -> CardLib.Card:
        if self.card_list:
            return self.card_list[-1]

    def update_cards_pos(self):
        for card in self.card_list:
            card.gui_obj.move(self.gui_obj.x, self.gui_obj.y)

    def gui_draw(self):
        if len(self) > 0:
            temp_card = self.card_list[-1]
            temp_card.gui_obj.draw()
        else:
            CardLib.gui.draw_rect((100, 100, 100), self.background_rect)
