
class Card:
    displayable = True
    suits = ['\u2660', '\u2665', '\u2663', '\u2666', '\u2605']
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "L", "H"]
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"[{Card.suits[self.suit]}{Card.ranks[self.rank]}]" if self.displayable else "[  ]"

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.rank == other.rank
        return False

    def set_display(self, display):
        self.displayable = display

    def __lt__(self, other):
        if self.rank == other.rank:
            return self.suit < other.suit
        else:
            return self.rank < other.rank
