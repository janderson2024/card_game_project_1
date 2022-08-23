from CardLib import CardList, Card
import CardLib

class DrawPile(CardList):
    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, 50, 50, self.gui_draw)

    def pop_card(self, display: bool = True) -> Card:
        card = self.card_list.pop()
        card.displayable = display
        return card

    def gui_draw(self):
        self.test_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, self.gui_obj.width, self.gui_obj.height)
        #print(self.test_rect)
        CardLib.gui.draw_rect((0,0,0), self.test_rect)
