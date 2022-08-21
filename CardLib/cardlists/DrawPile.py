from CardLib import CardList, Card
import CardLib

class DrawPile(CardList):
    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, 5, 90, self.gui_draw)

    def pop_card(self, display: bool = True) -> Card:
        card = self.card_list.pop()
        card.displayable = display
        return card
