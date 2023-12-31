import CardLib
from typing import Optional


class Card:
    displayable = True
    suits = [None, '\u2666', '\u2665', '\u2663', '\u2660']
    ranks = [None, "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "L", "H"]
    suit_text = [None, 'diamonds', 'hearts', 'clubs', 'spades']
    string_card_back = "[☼]"

    PATH_TO_IMG_DIR = "CardLib/card_images/standard/"

    def __init__(self, suit, rank, x=-1, y=-1, color='Red', displayable=True):
        self.suit = self.suits[int(suit)]
        self.rank = self.ranks[int(rank)]
        self.suit_val = suit
        self.value = rank
        self.suit_text = self.suit_text[int(suit)]
        self.color = self.update_color(color)
        self.image = self.update_face_image()
        self.displayable = displayable
        if self.rank == 'L' or self.rank == 'H':
            self.suit = '*'

        self._init_gui(x, y)

    def _init_gui(self, x, y):
        self.gui_obj = CardLib.gui.GuiObject(x, y, 62, 90, self.gui_draw)

        img_path = self.PATH_TO_IMG_DIR + self.image
        self.front_img = CardLib.gui.create_img(img_path, self.gui_obj.width, self.gui_obj.height)
        back_img = self.PATH_TO_IMG_DIR + "card_back.png"
        self.back_img = CardLib.gui.create_img(back_img, self.gui_obj.width, self.gui_obj.height)

    def __str__(self) -> str:
        return f"[{self.rank}{self.suit}]" if self.displayable else Card.string_card_back
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other) -> bool:
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def set_display(self):
        self.displayable = not self.displayable
        if self.displayable:
            self.image = self.update_face_image()
        else:
            self.image = 'card_back.png'

    def update_suit_text(self) -> Optional[str]:
        if self.suit == '\u2666':
            return "diamonds"
        elif self.suit == '\u2665':
            return "hearts"
        elif self.suit == '\u2663':
            return "clubs"
        elif self.suit == '\u2660':
            return "spades"
        else:
            return None

    def update_color(self, color: str) -> str:
        if self.suit == '\u2666' or self.suit == '\u2665' or self.rank == 'L':
            return 'Red'
        elif self.suit == '\u2663' or self.suit == '\u2660' or self.rank == 'H':
            return 'Black'
        else:
            return color

    def update_face_image(self) -> str:
        if self.rank == 'J':
            rank = 'jack'
        elif self.rank == 'Q':
            rank = 'queen'
        elif self.rank == 'K':
            rank = 'king'
        elif self.rank == 'A':
            rank = 'ace'
        else:
            rank = self.rank

        if self.rank == 'L':
            return "red_joker.png"
        if self.rank == 'H':
            return "black_joker.png"

        return f"{rank}_of_{self.suit_text}.png"

    def gui_draw(self):
        if self.displayable:
            CardLib.gui.draw_img(self.front_img, self.gui_obj.x, self.gui_obj.y)
        else:
            CardLib.gui.draw_img(self.back_img, self.gui_obj.x, self.gui_obj.y)
        #rect = CardLib.gui.create_rect(self.x, self.y, self.width, self.height)
        #f self.displayable:
            #color = (255, 255, 255)
        #else:
            #color = (0, 0, 0)
        #CardLib.gui.draw_rect(color, rect)