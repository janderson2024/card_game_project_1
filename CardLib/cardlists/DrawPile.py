from CardLib import CardList, Card
import CardLib

class DrawPile(CardList):
    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, 62, 90, self.gui_draw)
        self.background_rect = CardLib.gui.create_rect(self.gui_obj.x, self.gui_obj.y, self.gui_obj.width, self.gui_obj.height)
        
        self.PATH_TO_IMG_DIR = "CardLib/card_images/standard/"
        back_img = self.PATH_TO_IMG_DIR + "card_back.png"
        self.back_img = CardLib.gui.create_img(back_img, self.gui_obj.width, self.gui_obj.height)

    def pop_card(self, display: bool = True) -> Card:
        card = self.card_list.pop()
        card.displayable = display
        return card

    def update_cards_pos(self):
        for card in self.card_list:
            card.gui_obj.move(self.gui_obj.x, self.gui_obj.y)

    def gui_draw(self):
        CardLib.gui.draw_rect((100,100,100), self.background_rect)
        if len(self) > 0:
            CardLib.gui.draw_img(self.back_img, self.gui_obj.x, self.gui_obj.y)
        
        
