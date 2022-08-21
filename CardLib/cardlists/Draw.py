from CardLib import CardList, Card
import CardLib

class Draw(CardList):

    def pop_card(self, display: bool = True) -> Card:
        card = self.card_list.pop()
        card.displayable = display
        return card

    def gui_draw(self):
        if len(self) > 0:
            temp_card = self.card_list[-1]
            temp_card.gui_obj.draw()
        else:
            background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, 70, self.gui_obj.height)
            CardLib.gui.draw_rect((100, 100, 100), background_rect)