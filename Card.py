
class Card:
    displayable = True
    suits = ['\u2666', '\u2665', '\u2663', '\u2660']
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"[{Card.suits[self.suit]}{Card.ranks[self.rank]}]" if self.displayable else "[  ]"

    def set_display(self, display):
        self.displayable = display

    def __lt__(self, other):
        if self.rank == other.rank:
            return self.suit < other.suit
        else:
            return self.rank < other.rank
