from typing import Optional

import CardLib

class Card:
    string_card_back = "[;°Д°]"
    card_back_file_name = "card_back.png"

    def __init__(self, suit, rank, displayable=True):
        self.suit = CardLib.SUITS[suit]
        self.rank = CardLib.RANKS[rank]

        self.suit_val = suit
        self.value = rank

        self.suit_text = CardLib.suit_to_text(suit)

        self.img_file_name = self.get_img_file_name()

        self.displayable = displayable

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

    def flip_card(self):
        self.displayable = not self.displayable

    def get_img_file_name(self) -> str:
        rank = CardLib.rank_to_text(self.rank)

        if self.rank == 'L':
            return "low_Joker.png"
        if self.rank == 'H':
            return "high_Joker.png"

        return f"{rank}_of_{self.suit_text}.png"
