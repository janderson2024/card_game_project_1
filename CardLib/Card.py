class Card:
    displayable = True
    suits = [None, '\u2666', '\u2665', '\u2663', '\u2660']
    ranks = [None, "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A", "L", "H"]
    suit_text = [None, 'diamonds', 'hearts', 'clubs', 'spades']
    string_card_back = "[;°Д°]"

    def __init__(self, suit, rank, color='red', displayable=True):
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

    def __str__(self):
        return f"[{self.rank}{self.suit}]" if self.displayable else Card.string_card_back

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def __lt__(self, other):
        return self.value < other.value

    def set_display(self):
        self.displayable = not self.displayable
        if self.displayable:
            self.image = self.update_face_image()
        else:
            self.image = 'card_back.png'

    def update_suit_text(self):
        if self.suit == '\u2666':
            return "Diamonds"
        elif self.suit == '\u2665':
            return "Hearts"
        elif self.suit == '\u2663':
            return "Clubs"
        elif self.suit == '\u2660':
            return "Spades"
        else:
            return None

    def update_color(self, color):
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
